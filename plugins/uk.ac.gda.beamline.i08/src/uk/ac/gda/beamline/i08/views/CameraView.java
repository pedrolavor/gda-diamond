/*-
 * Copyright © 2010 Diamond Light Source Ltd.
 *
 * This file is part of GDA.
 *
 * GDA is free software: you can redistribute it and/or modify it under the
 * terms of the GNU General Public License version 3 as published by the Free
 * Software Foundation.
 *
 * GDA is distributed in the hope that it will be useful, but WITHOUT ANY
 * WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
 * details.
 *
 * You should have received a copy of the GNU General Public License along
 * with GDA. If not, see <http://www.gnu.org/licenses/>.
 */

package uk.ac.gda.beamline.i08.views;

import gda.configuration.properties.LocalProperties;
import gda.data.PathConstructor;
import gda.factory.FactoryException;
import gda.images.camera.ImageListener;
import gda.images.camera.RTPStreamReceiverSWT;
import gda.images.camera.VideoReceiver;

import org.dawnsci.plotting.jreality.tool.IImagePositionEvent;
import org.dawnsci.plotting.jreality.tool.ImagePositionListener;
import org.eclipse.draw2d.ColorConstants;
import org.eclipse.draw2d.geometry.Rectangle;
import org.eclipse.jface.action.Action;
import org.eclipse.jface.action.IToolBarManager;
import org.eclipse.jface.action.Separator;
import org.eclipse.swt.SWT;
import org.eclipse.swt.SWTException;
import org.eclipse.swt.events.MouseAdapter;
import org.eclipse.swt.events.MouseEvent;
import org.eclipse.swt.graphics.ImageData;
import org.eclipse.swt.graphics.ImageLoader;
import org.eclipse.swt.widgets.Composite;
import org.eclipse.swt.widgets.FileDialog;
import org.eclipse.swt.widgets.Label;
import org.eclipse.ui.part.ViewPart;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import uk.ac.gda.beamline.i08.I08BeamlineActivator;
import uk.ac.gda.client.microfocus.views.BeamCentreFigure;
import uk.ac.gda.client.viewer.ImageViewer;

public class CameraView extends ViewPart {
	public static final String ID = "uk.ac.gda.beamline.i08.cameraView";
	private static final Logger logger = LoggerFactory.getLogger(CameraView.class);
	private ImageViewer viewer;
	private VideoReceiver<ImageData> videoReceiver;
	private ImageListener<ImageData> listener = new VideoListener();
	private Rectangle beamCentreFigurePosition = new Rectangle(0, 0, -1, -1);
	private Action openFiles;
	private Action resetView;
	private Action start;
	private Action stop;
	private BeamCentreFigure beamCentreFigure;
	private boolean layoutReset;
	private Action snap;
	private String snapDirectory = PathConstructor.createFromProperty("gda.cameraview.snapshot.dir");

	public CameraView() {
	}

	@Override
	public void createPartControl(Composite parent) {

		String ip = LocalProperties.get("gda.cameraview.rtp.ip");
		String port = LocalProperties.get("gda.cameraview.rtp.port");
		
		if (ip!=null && port!=null) {
			
			viewer = new ImageViewer(parent, SWT.DOUBLE_BUFFERED);
			RTPStreamReceiverSWT r = new RTPStreamReceiverSWT();
			r.setHost(ip);
			r.setPort(Integer.parseInt(port));
			try {
				r.configure();
			} catch (FactoryException e) {
				logger.error("Unable to configure the video receiver ", e);
			}
			videoReceiver = r;
			videoReceiver.addImageListener(listener);
			videoReceiver.start();
			initializeToolBar();
		}
		else
			new Label(parent, SWT.NONE).setText("No rtp stream properties defined. gda.cameraview.rtp.ip and gda.cameraview.rtp.port");
	}

	@Override
	public void setFocus() {
		viewer.setFocus();
	}

	@Override
	public void dispose() {
		super.dispose();
		videoReceiver.stop();
		viewer.dispose();
		videoReceiver.removeImageListener(listener);
	}

	private void initializeToolBar() {
		IToolBarManager toolbarManager = getViewSite().getActionBars().getToolBarManager();

		openFiles = new Action() {
			@Override
			public void run() {
				viewer.onFileOpen();
			}
		};
		openFiles.setText("Open File");
		openFiles.setToolTipText("Opens browser to locate an image file on disk");
		openFiles.setImageDescriptor(I08BeamlineActivator.getImageDescriptor("icons/folder_camera.png"));

		resetView = new Action() {
			@Override
			public void run() {
				viewer.resetView();
			}
		};
		resetView.setText("Reset view");
		resetView.setToolTipText("Reset panning and zooming");
		resetView.setImageDescriptor(I08BeamlineActivator.getImageDescriptor("icons/page_refresh.png"));
		start = new Action() {
			@Override
			public void run() {
				videoReceiver.start();
			}
		};
		start.setText("Start");
		start.setToolTipText("Start video capture");
		start.setImageDescriptor(I08BeamlineActivator.getImageDescriptor("icons/camera.png"));
		stop = new Action() {
			@Override
			public void run() {
				videoReceiver.stop();
			}
		};
		stop.setText("stop");
		stop.setToolTipText("stop video capture");
		stop.setImageDescriptor(I08BeamlineActivator.getImageDescriptor("icons/stop.png"));

		snap = new Action() {
			@Override
			public void run() {
				FileDialog fileChooser = new FileDialog(viewer.getCanvas().getShell(), SWT.SAVE);
				fileChooser.setText("Save image file");
				fileChooser.setFilterPath(snapDirectory);
				fileChooser.setFilterExtensions(new String[] { "*.jpg" });
				fileChooser.setFilterNames(new String[] { "SWT image" + " (jpg)" });
				String filename = fileChooser.open();
				if (filename != null)
					saveImage(filename, fileChooser.getFilterExtensions()[0]);
			}
		};
		snap.setText("Snapshot");
		snap.setToolTipText("Snap shot");
		snap.setImageDescriptor(I08BeamlineActivator.getImageDescriptor("icons/folder_camera.png"));

		toolbarManager.add(new Separator());
		toolbarManager.add(openFiles);
		toolbarManager.add(resetView);
		toolbarManager.add(new Separator());
		toolbarManager.add(start);
		toolbarManager.add(stop);
		toolbarManager.add(snap);
	}

	public void saveImage(String filename, String format) {
		ImageLoader loader = new ImageLoader();
		loader.data = new ImageData[] { viewer.getImageData() };
		try {
			logger.info("Trying to save file " + filename + " of the format " + format);
			if (loader.data != null && loader.data.length != 0 && loader.data[0] != null)
				loader.save(filename, SWT.IMAGE_JPEG);
			else
				logger.error("No image available");
		} catch (SWTException e) {
			logger.error("problem saving the image as " + format + "in file " + filename, e);
		}
	}

	private void initializeListeners() {
		viewer.getCanvas().addMouseListener(new MouseAdapter() {

			@Override
			public void mouseDown(MouseEvent event) {
				logger.debug("Mouse Down");
			}

			@Override
			public void mouseUp(MouseEvent event) {
				logger.debug("Mouse Up");
			}

			@Override
			public void mouseDoubleClick(MouseEvent event) {
				logger.debug("Mouse Double Clicked");
			}
		});

		ImagePositionListener newListener = new ImagePositionListener() {
			@Override
			public void imageStart(IImagePositionEvent event) {
				double[] position = event.getPosition();
				int[] imagePosition = event.getImagePosition();
				updateStatus((int) position[0], (int) position[1], imagePosition[0], imagePosition[1]);
			}

			@Override
			public void imageFinished(IImagePositionEvent event) {
				double[] position = event.getPosition();
				int[] imagePosition = event.getImagePosition();
				updateStatus((int) position[0], (int) position[1], imagePosition[0], imagePosition[1]);
			}

			@Override
			public void imageDragged(IImagePositionEvent event) {
				double[] position = event.getPosition();
				int[] imagePosition = event.getImagePosition();
				updateStatus((int) position[0], (int) position[1], imagePosition[0], imagePosition[1]);
			}
		};
		viewer.getPositionTool().addImagePositionListener(newListener, null);
	}

	private void updateStatus(int x, int y, int ix, int iy) {
		logger.debug("Mouse position at: (" + x + ", " + y + ")");
		logger.debug("Image position at: (" + ix + ", " + iy + ")");
	}

	private void initViewer() {
		if (!layoutReset) {
			layoutReset = true;
			viewer.getCanvas().getDisplay().asyncExec(new Runnable() {
				@Override
				public void run() {
					viewer.resetView();
					initializeBeamFigures();
					updateBeamCentreFigure();
				}
			});
		}
	}

	private void updateBeamCentreFigure() {
		int x = (viewer.getImageData().width - beamCentreFigure.getCrossHairSize().width) / 2;
		int y = (viewer.getImageData().height - beamCentreFigure.getCrossHairSize().height) / 2;
		beamCentreFigurePosition = new Rectangle(x, y, -1, -1);
		viewer.getTopFigure().setConstraint(beamCentreFigure, beamCentreFigurePosition);
	}

	private void initializeBeamFigures() {
		if (beamCentreFigure == null) {
			beamCentreFigure = new BeamCentreFigure();
			beamCentreFigure.setForegroundColor(ColorConstants.red);
			viewer.getTopFigure().add(beamCentreFigure, new Rectangle(0, 0, -1, -1));
		}
	}

	private final class VideoListener implements ImageListener<ImageData> {
		private String name;

		@Override
		public void setName(String name) {
			this.name = name;
		}

		@Override
		public String getName() {
			return name;
		}

		@Override
		public void processImage(ImageData image) {
			if (image == null)
				return;
			if (viewer != null) {
				viewer.loadImage(image);
				initViewer();
			}
		}
	}
}
