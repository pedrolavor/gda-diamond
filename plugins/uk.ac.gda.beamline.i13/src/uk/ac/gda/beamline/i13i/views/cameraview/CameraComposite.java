/*-
 * Copyright © 2011 Diamond Light Source Ltd.
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

package uk.ac.gda.beamline.i13i.views.cameraview;

import gda.images.camera.ImageListener;
import gda.images.camera.VideoReceiver;

import org.eclipse.draw2d.IFigure;
import org.eclipse.jface.layout.GridDataFactory;
import org.eclipse.swt.SWT;
import org.eclipse.swt.graphics.ImageData;
import org.eclipse.swt.layout.GridLayout;
import org.eclipse.swt.widgets.Composite;
import org.eclipse.swt.widgets.Display;
import org.eclipse.swt.widgets.Event;
import org.eclipse.swt.widgets.Listener;
import org.eclipse.ui.PlatformUI;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import uk.ac.diamond.scisoft.analysis.dataset.AbstractDataset;
import uk.ac.diamond.scisoft.analysis.dataset.IDataset;
import uk.ac.diamond.scisoft.analysis.rcp.plotting.utils.SWTImageUtils;
import uk.ac.gda.client.viewer.ImageViewer;


public class CameraComposite extends Composite {

	static final Logger logger = LoggerFactory.getLogger(CameraComposite.class);
	ImageViewer viewer;
	private VideoReceiver<ImageData> videoReceiver;
	private VideoListener listener;


	Composite parent;

	NewImageListener newImageListener;
	public CameraComposite(Composite parent, int style, @SuppressWarnings("unused") Display display,NewImageListener newImageListener) {
		super(parent, style);
		this.newImageListener = newImageListener;

		setLayout(new GridLayout(1, false));
		viewer = new uk.ac.gda.client.viewer.ImageViewer(this, SWT.DOUBLE_BUFFERED);
		GridDataFactory.fillDefaults().grab(true, true).applyTo(viewer.getCanvas());

		viewer.showDefaultImage();

		viewer.getCanvas().addListener(SWT.Resize, new Listener() {
			@Override
			public void handleEvent(Event event) {
				zoomFit();
			}
		});
		zoomFit();
		pack();
	}
	
	private void disconnectFromReceiver(){
		if( videoReceiver != null && listener != null){
			videoReceiver.removeImageListener(listener);
			videoReceiver = null;
		}
		
	}
	public void setVideoReceiver(VideoReceiver<ImageData> videoReceiver) {
		disconnectFromReceiver();
		if( listener == null){
			listener = new VideoListener();
		}
		this.videoReceiver = videoReceiver;
		if( videoReceiver != null){
			this.videoReceiver.addImageListener(listener);
		}
	}

	public IFigure getTopFigure() {
		return viewer.getTopFigure();
	}

	boolean layoutReset = false;

	@Override
	public boolean setFocus() {
		return viewer != null ? viewer.setFocus() : false;
	}

	@Override
	public void dispose() {
		super.dispose();
		disconnectFromReceiver();
		viewer.dispose();
	}

	public void zoomFit() {
		if (viewer != null)
			viewer.zoomFit();
	}
	public IDataset getDataset(){
		return lastImage != null ? new SWTImageDataConverter(lastImage).toIDataset() : null;
	}

	ImageData lastImage;
	private final class VideoListener implements ImageListener<ImageData> {
		private String name;

		@Override
		public void setName(String name) {
			this.name = name;
		}

		@SuppressWarnings("unused")
		public void clear() {
			viewer.showDefaultImage();
		}

		@Override
		public String getName() {
			return name;
		}

		boolean processingImage=false;
		
		NewImageHnadler latestUpdater = null;
		@Override
		public void processImage(final ImageData image) {
			if (image == null)
				return;
			
			
			if (viewer != null) {
				if(isDisposed())
					return;
/*				if(processingImage)
					return;
				processingImage=true;
				try {
					Thread.sleep(100);
				} catch (InterruptedException e) {
					throw new RuntimeException("processImage interrupted");
				}
*/				if( getDisplay().isDisposed())
					return;
				
				lastImage=image;
				
				if( latestUpdater ==null || !latestUpdater.inqueue){
					latestUpdater = new NewImageHnadler(CameraComposite.this);
					if (!PlatformUI.getWorkbench().getDisplay().isDisposed()) {
						PlatformUI.getWorkbench().getDisplay().asyncExec(latestUpdater);
					}
				}
				
/*				getDisplay().asyncExec(new Runnable() {
					@Override
					public void run() {
						boolean showingDefault = viewer.isShowingDefault();
						while(true){
							//ensure we don't miss an image that arrives while we process the first
								ImageData lastImage2 = lastImage;
								viewer.loadImage(lastImage2);
								if (showingDefault) {
									zoomFit();
								}
								if (!layoutReset){
									layoutReset = true;
									viewer.resetView();
								}

								if( newImageListener != null){
									try {
										newImageListener.handlerNewImageNotification(lastImage2);
									} catch (Exception e) {
										logger.error("Error in handling new image", e);
									}
								}
								if( lastImage2 == lastImage){
									processingImage=false;
									break;
								}
								processingImage=false;
								break; //TODO we may remain in UI thread if frame rate is very high
						}
					}
				});
*/			}
		}
	}
	public ImageViewer getViewer() {
		return viewer;
	}
}

class SWTImageDataConverter {
	ImageData imageData;
	IDataset idataset;

	public SWTImageDataConverter(ImageData imageData) {
		this.imageData = imageData;
	}

	public IDataset toIDataset() {
		if (imageData == null) {
			return null;
		}
		if( idataset == null){
			idataset = SWTImageUtils.createRGBDataset(imageData).createGreyDataset(AbstractDataset.FLOAT32);
		}
		return idataset;

	}
}

class NewImageHnadler implements Runnable{
	public boolean inqueue;

	
	CameraComposite listener;
	
	
	public NewImageHnadler(CameraComposite listener) {
		super();
		this.listener = listener;
		inqueue=true;
	}


	@Override
	public void run() {
		inqueue = false; 
		boolean showingDefault = listener.viewer.isShowingDefault();
		//ensure we don't miss an image that arrives while we process the first
		ImageData lastImage2 = listener.lastImage;
		listener.viewer.loadImage(lastImage2);
		if (showingDefault) {
			listener.zoomFit();
		}
		if (!listener.layoutReset){
			listener.layoutReset = true;
			listener.viewer.resetView();
		}

		if( listener.newImageListener != null){
			try {
				listener.newImageListener.handlerNewImageNotification(lastImage2);
			} catch (Exception e) {
				CameraComposite.logger.error("Error in handling new image", e);
			}
		}
	}
	
}


