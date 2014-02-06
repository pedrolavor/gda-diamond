/*-
 * Copyright © 2013 Diamond Light Source Ltd.
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

package uk.ac.gda.beamline.i13i.ADViewerImpl;

import gda.device.ScannableMotionUnits;
import gda.device.scannable.ScannablePositionChangeEvent;
import gda.device.scannable.ScannableStatus;
import gda.device.scannable.ScannableUtils;
import gda.observable.IObserver;

import java.util.Vector;

import org.apache.commons.math.linear.MatrixUtils;
import org.apache.commons.math.linear.RealVector;
import org.eclipse.draw2d.ColorConstants;
import org.eclipse.draw2d.RectangleFigure;
import org.eclipse.draw2d.geometry.Rectangle;
import org.eclipse.jface.action.Action;
import org.eclipse.jface.action.IAction;
import org.eclipse.jface.action.IToolBarManager;
import org.eclipse.jface.dialogs.MessageDialog;
import org.eclipse.swt.SWT;
import org.eclipse.swt.events.SelectionEvent;
import org.eclipse.swt.events.SelectionListener;
import org.eclipse.swt.graphics.Cursor;
import org.eclipse.swt.graphics.ImageData;
import org.eclipse.swt.widgets.Display;
import org.eclipse.swt.widgets.Menu;
import org.eclipse.swt.widgets.MenuItem;
import org.eclipse.ui.IActionBars;
import org.eclipse.ui.PlatformUI;

import uk.ac.gda.beamline.i13i.DisplayScaleProvider;
import uk.ac.gda.epics.adviewer.composites.MJPeg;
import uk.ac.gda.epics.adviewer.composites.imageviewer.IImagePositionEvent;
import uk.ac.gda.epics.adviewer.composites.imageviewer.ImagePositionListener;
import uk.ac.gda.epics.adviewer.views.MJPegView;

public class I13MJPegViewInitialiser  {

	I13ADControllerImpl adControllerImpl;
	boolean changeRotationAxisX, changeImageMarker, vertMoveOnClickEnabled, horzMoveOnClickEnabled;
	private RectangleFigure rotationAxisFigure;

	RectangleFigure imageMarkerFigureX, imageMarkerFigureY;

	private MJPeg mJPeg;
	MJPegView mjPegView;

	public I13MJPegViewInitialiser(I13ADControllerImpl adController, MJPeg mJPeg, MJPegView mjPegView) {
		super();
		this.adControllerImpl = adController;
		this.mJPeg = mJPeg;
		this.mjPegView = mjPegView;

		Menu rightClickMenu = new Menu(mJPeg.getCanvas());
		MenuItem setRotationAxisX = new MenuItem(rightClickMenu, SWT.PUSH);
		setRotationAxisX.setText("Mark next click position as rotationAxisX");
		setRotationAxisX.addSelectionListener(new SelectionListener() {

			@Override
			public void widgetSelected(SelectionEvent event) {
				final Cursor cursorWait = new Cursor(Display.getDefault(), SWT.CURSOR_HAND);
				Display.getDefault().getActiveShell().setCursor(cursorWait);
				changeRotationAxisX = true;
			}

			@Override
			public void widgetDefaultSelected(SelectionEvent event) {
				widgetSelected(event);
			}
		});

		MenuItem setImageMarker = new MenuItem(rightClickMenu, SWT.PUSH);
		setImageMarker.setText("Mark next click position as beam centre");
		setImageMarker.addSelectionListener(new SelectionListener() {

			@Override
			public void widgetSelected(SelectionEvent event) {
				final Cursor cursorWait = new Cursor(Display.getDefault(), SWT.CURSOR_HAND);
				Display.getDefault().getActiveShell().setCursor(cursorWait);
				changeImageMarker = true;
			}

			@Override
			public void widgetDefaultSelected(SelectionEvent event) {
				final Cursor cursorWait = new Cursor(Display.getCurrent(), SWT.CURSOR_HAND);
				Display.getDefault().getActiveShell().setCursor(cursorWait);
				changeImageMarker = true;
			}
		});

		mJPeg.getCanvas().setMenu(rightClickMenu);

		mJPeg.addImagePositionListener(new ImagePositionListener() {

			@Override
			public void imageStart(IImagePositionEvent event) {
			}

			@Override
			public void imageFinished(IImagePositionEvent event) {
				if (changeRotationAxisX) {
					int beamCentreX = event.getImagePosition()[0];
					int beamCentreY = event.getImagePosition()[1];
					boolean changeCentre = MessageDialog.openQuestion(
							PlatformUI.getWorkbench().getDisplay().getActiveShell(),
							"Change Beam Centre",
							"Are you sure you wish to change the rotation axis to this position ("
									+ Integer.toString(beamCentreX) + "," + Integer.toString(beamCentreY) + "?");
					if (changeCentre) {
						try {
							final int[] clickCoordinates = event.getImagePosition();
							final RealVector actualClickPoint = createVectorOf(clickCoordinates[0], clickCoordinates[1]);
							ImageData imageData = I13MJPegViewInitialiser.this.mJPeg.getImageData();
							final RealVector imageDataSize = createVectorOf(imageData.width, imageData.height);
							final RealVector imageSize = createVectorOf((adControllerImpl).getFfmpegImageInWidth(),
									adControllerImpl.getFfmpegImageInHeight());

							final RealVector clickPointInImage = actualClickPoint.ebeMultiply(imageSize).ebeDivide(
									imageDataSize);

							// The image is reflected so we need to subtract from width
							adControllerImpl.getRotationAxisXScannable().asynchronousMoveTo(
									imageSize.getEntry(0) - clickPointInImage.getEntry(0));
						} catch (Exception e) {
							MJPegView.reportErrorToUserAndLog("Error setting rotationAxis", e);
						}
					}
					changeRotationAxisX = false;
					final Cursor cursorWait = new Cursor(Display.getCurrent(), SWT.CURSOR_ARROW);
					Display.getDefault().getActiveShell().setCursor(cursorWait);
				} else if (changeImageMarker) {
					int beamCentreX = event.getImagePosition()[0];
					int beamCentreY = event.getImagePosition()[1];
					boolean changeCentre = MessageDialog.openQuestion(
							PlatformUI.getWorkbench().getDisplay().getActiveShell(),
							"Change beam centre marker",
							"Are you sure you wish to change the beam centre marker to this position ("
									+ Integer.toString(beamCentreX) + "," + Integer.toString(beamCentreY) + "?");
					if (changeCentre) {
						try {
							final int[] clickCoordinates = event.getImagePosition();
							final RealVector actualClickPoint = createVectorOf(clickCoordinates[0], clickCoordinates[1]);
							ImageData imageData = I13MJPegViewInitialiser.this.mJPeg.getImageData();
							final RealVector imageDataSize = createVectorOf(imageData.width, imageData.height);
							final RealVector imageSize = createVectorOf(adControllerImpl.getFfmpegImageInWidth(),
									adControllerImpl.getFfmpegImageInHeight());

							final RealVector clickPointInImage = actualClickPoint.ebeMultiply(imageSize).ebeDivide(
									imageDataSize);

							// The image is reflected so we need to subtract from width
							// we also want height from the bottom up so subtract from height
							adControllerImpl.getCameraXYScannable().asynchronousMoveTo(
									new double[] { imageSize.getEntry(0) - clickPointInImage.getEntry(0),
											imageSize.getEntry(1) - clickPointInImage.getEntry(1) });
						} catch (Exception e) {
							MJPegView.reportErrorToUserAndLog("Error setting beam centre marker", e);
						}
					}
					changeImageMarker = false;
					final Cursor cursorWait = new Cursor(Display.getCurrent(), SWT.CURSOR_ARROW);
					Display.getDefault().getActiveShell().setCursor(cursorWait);
				} else if (vertMoveOnClickEnabled || horzMoveOnClickEnabled) {
					try {
						final int[] clickCoordinates = event.getImagePosition();
						final RealVector actualClickPoint = createVectorOf(clickCoordinates[0], clickCoordinates[1]);
						ImageData imageData = I13MJPegViewInitialiser.this.mJPeg.getImageData();
						final RealVector imageDataSize = createVectorOf(imageData.width, imageData.height);
						final RealVector imageSize = createVectorOf(adControllerImpl.getFfmpegImageInWidth(),
								adControllerImpl.getFfmpegImageInHeight());

						RealVector clickPointInImage = actualClickPoint.ebeMultiply(imageSize).ebeDivide(imageDataSize);

						// correct for left right reflection
						// beam Centre is measure from bottom whilst clickPoint is from top
						final RealVector clickPointInImageCorrected = imageSize.subtract(clickPointInImage);
						double beamCenterX = ScannableUtils.getCurrentPositionArray(adControllerImpl
								.getRotationAxisXScannable())[0];
						double beamCenterY = ScannableUtils.getCurrentPositionArray(adControllerImpl
								.getCameraXYScannable())[1];
						final RealVector beamCenterV = createVectorOf(beamCenterX, beamCenterY);
						final RealVector pixelOffset = beamCenterV.subtract(clickPointInImageCorrected);

						DisplayScaleProvider scale = adControllerImpl.getCameraScaleProvider();

						if( vertMoveOnClickEnabled){
							double moveInY = pixelOffset.getEntry(1) / scale.getPixelsPerMMInY();

							ScannableMotionUnits sampleCentringYMotor = adControllerImpl.getSampleCentringYMotor();
							sampleCentringYMotor.asynchronousMoveTo(ScannableUtils
									.getCurrentPositionArray(sampleCentringYMotor)[0] + moveInY);
							
						}
						if( horzMoveOnClickEnabled){
							double moveInX = pixelOffset.getEntry(0) / scale.getPixelsPerMMInX();
	
							ScannableMotionUnits sampleCentringXMotor = adControllerImpl.getSampleCentringXMotor();
							sampleCentringXMotor.asynchronousMoveTo(ScannableUtils
									.getCurrentPositionArray(sampleCentringXMotor)[0] + moveInX);
						}
					} catch (Exception e) {
						MJPegView.reportErrorToUserAndLog("Error processing imageFinished", e);
					}
				}

			}

			@Override
			public void imageDragged(IImagePositionEvent event) {
			}
		}, null);

		Vector<Action> showActions = new Vector<Action>();

		final Action rotationAxisAction = new Action("Show rotation axis", IAction.AS_CHECK_BOX) {
			@Override
			public void run() {
				try {
					showRotationAxis(isChecked());
				} catch (Exception e) {
					MJPegView.reportErrorToUserAndLog("Error showing rotation axis", e);
				}
			}
		};
		try {
			showRotationAxis(true);
			rotationAxisAction.setChecked(true);// do not
		} catch (Exception e) {
			MJPegView.reportErrorToUserAndLog("Error showing rotation axis", e);
		}
		final Action showImageMarkerAction = new Action("Show beam centre", IAction.AS_CHECK_BOX) {
			@Override
			public void run() {
				try {
					showImageMarker(isChecked());
				} catch (Exception e) {
					MJPegView.reportErrorToUserAndLog("Error showing beam centre", e);
				}
			}
		};
		try {
			showImageMarker(true);
			showImageMarkerAction.setChecked(true);// do not
		} catch (Exception e) {
			MJPegView.reportErrorToUserAndLog("Error showing beam centre", e);
		}

		showActions.add(rotationAxisAction);
		showActions.add(showImageMarkerAction);

		MenuCreator showMenu = new MenuCreator("Show",
				"Actions that lead to items shown on the image or in other views", showActions);

/*		moveOnClickAction = new Action("Move Sample On Click", IAction.AS_CHECK_BOX) {
			@Override
			public void run() {
				moveOnClickEnabled = !moveOnClickEnabled;
			}
		};
		moveOnClickAction.setChecked(false);// do not

		Vector<Action> moveActions = new Vector<Action>();
		moveActions.add(moveOnClickAction);

		MenuCreator moveMenu = new MenuCreator("Alignment", "Actions that move the camera and sample stages",
				moveActions);
*/
		IActionBars actionBars = mjPegView.getViewSite().getActionBars();
		IToolBarManager toolBar = actionBars.getToolBarManager();
		toolBar.add(showMenu);
//		toolBar.add(moveMenu);

		rotationAxisObserver = new IObserver() {

			@Override
			public void update(Object source, final Object arg) {
				if (rotationAxisAction.isChecked()) {
					if ((arg instanceof ScannableStatus && (((ScannableStatus) arg).status == ScannableStatus.IDLE))
							|| (arg instanceof ScannablePositionChangeEvent)) {
						showRotationAxisFromNonUIThread(rotationAxisAction);
					}
				}
			}

		};
		adControllerImpl.getRotationAxisXScannable().addIObserver(rotationAxisObserver);

		cameraXYObserver = new IObserver() {

			@Override
			public void update(Object source, final Object arg) {
				if ((arg instanceof ScannableStatus && (((ScannableStatus) arg).status == ScannableStatus.IDLE))
						|| (arg instanceof ScannablePositionChangeEvent)) {
					showImageMarkerFromNonUIThread(showImageMarkerAction);
				}
			}

		};
		adControllerImpl.getCameraXYScannable().addIObserver(cameraXYObserver);

		showRotationAxisFromNonUIThread(rotationAxisAction);
		showImageMarkerFromNonUIThread(showImageMarkerAction);

	}

	private void showRotationAxisFromNonUIThread(final Action rotationAxisAction) {
		if (rotationAxisAction.isChecked()) {

			mjPegView.getViewSite().getShell().getDisplay().asyncExec(new Runnable() {

				@Override
				public void run() {
					try {
						showRotationAxis(true);
					} catch (Exception e) {
						MJPegView.reportErrorToUserAndLog("Error showing rotation axis", e);
					}

				}
			});
		}
	}

	private void showImageMarkerFromNonUIThread(final Action showImageMarkerAction) {
		if (showImageMarkerAction.isChecked()) {
			mjPegView.getViewSite().getShell().getDisplay().asyncExec(new Runnable() {

				@Override
				public void run() {
					try {
						showImageMarker(true);
					} catch (Exception e) {
						MJPegView.reportErrorToUserAndLog("Error showing beam centre", e);
					}

				}
			});
		}
	}

	void showRotationAxis(boolean show) throws Exception {
		RectangleFigure rotationAxisFigure = getRotationAxisFigure();
		if (rotationAxisFigure.getParent() == mJPeg.getTopFigure())
			mJPeg.getTopFigure().remove(rotationAxisFigure);
		if (show) {
			int rotationAxisX = (int) ScannableUtils.getCurrentPositionArray(adControllerImpl
					.getRotationAxisXScannable())[0];
			org.eclipse.draw2d.geometry.Rectangle bounds = rotationAxisFigure.getBounds();
			int ffmpegImageInWidth = adControllerImpl.getFfmpegImageInWidth();
			// the image is reflected so subtract from full width to get position on the screen
			int pixelInImage = ffmpegImageInWidth - rotationAxisX;

			ImageData imageData = mJPeg.getImageData();
			int width = imageData.width;
			int height = imageData.height;
			int x = pixelInImage * width / ffmpegImageInWidth;
			// ensure the axis is not shown off the image
			int constraintX = x - bounds.width / 2;

			int maxConstraintX = width - widthOffAxis / 2;
			int minConstraintX = widthOffAxis / 2;
			constraintX = Math.min(constraintX, maxConstraintX);
			constraintX = Math.max(constraintX, minConstraintX);

			boolean offAxis = constraintX == minConstraintX || constraintX == maxConstraintX;
			rotationAxisFigure.setSize(offAxis ? widthOffAxis : 5, height);
			rotationAxisFigure.setAlpha(offAxis ? 100 : 50);
			rotationAxisFigure.setLineWidth(offAxis ? widthOffAxis : 5);

			mJPeg.getTopFigure().add(rotationAxisFigure, new Rectangle(constraintX, 0, -1, -1));

		}
	}

	private RectangleFigure getRotationAxisFigure() {
		if (rotationAxisFigure == null) {
			rotationAxisFigure = new RectangleFigure();
			rotationAxisFigure.setFill(true);
			rotationAxisFigure.setSize(5, adControllerImpl.getCameraImageHeightMax());
			rotationAxisFigure.setLineWidth(5);
			rotationAxisFigure.setForegroundColor(ColorConstants.red);
			rotationAxisFigure.setAlpha(50);
		}
		return rotationAxisFigure;
	}

	static int widthOffAxis = 20;
	static int widthOffAxisHalf = widthOffAxis / 2;
	private IObserver rotationAxisObserver;
	private IObserver cameraXYObserver;
	public Action moveOnClickAction;

	void showImageMarker(boolean show) throws Exception {
		RectangleFigure imageMarkerFigureX = getImageMarkerFigureX();
		if (imageMarkerFigureX.getParent() == mJPeg.getTopFigure())
			mJPeg.getTopFigure().remove(imageMarkerFigureX);
		if (show) {
			double[] pos = ScannableUtils.getCurrentPositionArray(adControllerImpl.getCameraXYScannable());
			int imageMarkerY = (int) pos[1];
			Rectangle bounds = imageMarkerFigureX.getBounds();
			ImageData imageData = mJPeg.getImageData();
			int ffmpegImageInHeight = adControllerImpl.getFfmpegImageInHeight();
			// the image is reflected so subtract from full width to get position on the screen
			// ensure the axis is not shown off the image

			// y is measure from top down but imageMarkY is from bottom up
			int pixelInImageY = ffmpegImageInHeight - imageMarkerY;
			int height = imageData.height;
			int y = (pixelInImageY * height / ffmpegImageInHeight);

			int halfHeight = bounds.height / 2;
			int constraintY = y - halfHeight;

			int maxConstraintY = height - halfHeight - widthOffAxisHalf;
			int minConstraintY = widthOffAxisHalf - halfHeight;
			constraintY = Math.min(constraintY, maxConstraintY);
			constraintY = Math.max(constraintY, minConstraintY);

			boolean offAxis = constraintY == minConstraintY || constraintY == maxConstraintY;
			imageMarkerFigureX.setSize(imageData.width, offAxis ? widthOffAxis : 5);
			imageMarkerFigureX.setAlpha(offAxis ? 100 : 50);
			imageMarkerFigureX.setLineWidth(offAxis ? widthOffAxis : 5);

			mJPeg.getTopFigure().add(imageMarkerFigureX, new Rectangle(0, constraintY, -1, -1));

		}
		RectangleFigure imageMarkerFigureY = getImageMarkerFigureY();
		if (imageMarkerFigureY.getParent() == mJPeg.getTopFigure())
			mJPeg.getTopFigure().remove(imageMarkerFigureY);
		if (show) {
			double[] pos = ScannableUtils.getCurrentPositionArray(adControllerImpl.getCameraXYScannable());
			int imageMarkerX = (int) pos[0];
			Rectangle bounds = imageMarkerFigureY.getBounds();
			ImageData imageData = mJPeg.getImageData();
			int ffmpegImageInWidth = adControllerImpl.getFfmpegImageInWidth();
			// the image is reflected so subtract from full width to get position on the screen
			// ensure the axis is not shown off the image

			int pixelInImageX = ffmpegImageInWidth - imageMarkerX;
			int width = imageData.width;
			int x = pixelInImageX * width / ffmpegImageInWidth;
			int halfWidth = bounds.width / 2;
			int constraintX = x - halfWidth;

			int maxConstraintX = width - halfWidth - widthOffAxisHalf;
			int minConstraintX = widthOffAxisHalf - halfWidth;
			constraintX = Math.min(constraintX, maxConstraintX);
			constraintX = Math.max(constraintX, minConstraintX);

			boolean offAxis = constraintX == minConstraintX || constraintX == maxConstraintX;

			imageMarkerFigureY.setSize(offAxis ? widthOffAxis : 5, imageData.height);
			imageMarkerFigureY.setAlpha(offAxis ? 100 : 50);
			imageMarkerFigureY.setLineWidth(offAxis ? widthOffAxis : 5);

			mJPeg.getTopFigure().add(imageMarkerFigureY, new Rectangle(constraintX, 0, -1, -1));

		}
	}

	private RectangleFigure getImageMarkerFigureX() {
		if (imageMarkerFigureX == null) {
			imageMarkerFigureX = new RectangleFigure();
			imageMarkerFigureX.setFill(true);
			imageMarkerFigureX.setSize(adControllerImpl.getCameraImageWidthMax(), 5);
			imageMarkerFigureX.setLineWidth(5);
			imageMarkerFigureX.setForegroundColor(ColorConstants.lightBlue);
			imageMarkerFigureX.setAlpha(50);
		}
		return imageMarkerFigureX;
	}

	private RectangleFigure getImageMarkerFigureY() {
		if (imageMarkerFigureY == null) {
			imageMarkerFigureY = new RectangleFigure();
			imageMarkerFigureY.setFill(true);
			imageMarkerFigureY.setSize(5, adControllerImpl.getCameraImageHeightMax());
			imageMarkerFigureY.setLineWidth(5);
			imageMarkerFigureY.setForegroundColor(ColorConstants.lightBlue);
			imageMarkerFigureY.setAlpha(50);
		}
		return imageMarkerFigureY;
	}

	static RealVector createVectorOf(double... data) {
		return MatrixUtils.createRealVector(data);
	}

	void  dispose(){
		if( rotationAxisObserver != null ){
			adControllerImpl.getRotationAxisXScannable().deleteIObserver(rotationAxisObserver);
			rotationAxisObserver = null;
		}
		if( cameraXYObserver != null ){
			adControllerImpl.getCameraXYScannable().deleteIObserver(cameraXYObserver);
			cameraXYObserver = null;
		}
		
	}

	public void setVertMoveOnClick(boolean selection) {
		vertMoveOnClickEnabled = selection;
	}
	public void setHorzMoveOnClick(boolean selection) {
		horzMoveOnClickEnabled = selection;
	}
}
