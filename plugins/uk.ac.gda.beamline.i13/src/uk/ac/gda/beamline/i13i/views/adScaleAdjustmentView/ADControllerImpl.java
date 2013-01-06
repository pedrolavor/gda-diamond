/*-
 * Copyright © 2012 Diamond Light Source Ltd.
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

package uk.ac.gda.beamline.i13i.views.adScaleAdjustmentView;

import gda.device.Scannable;
import gda.device.detector.areadetector.v17.ADBase;
import gda.device.detector.areadetector.v17.FfmpegStream;
import gda.device.detector.areadetector.v17.NDArray;
import gda.device.detector.areadetector.v17.NDPluginBase;
import gda.device.detector.areadetector.v17.NDProcess;
import gda.device.detector.areadetector.v17.NDStats;
import gda.jython.InterfaceProvider;
import gda.observable.Observable;
import gda.observable.Observer;

import org.eclipse.jface.layout.GridDataFactory;
import org.eclipse.swt.SWT;
import org.eclipse.swt.layout.FillLayout;
import org.eclipse.swt.widgets.Composite;
import org.eclipse.ui.part.ViewPart;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.InitializingBean;

import uk.ac.diamond.scisoft.analysis.dataset.DoubleDataset;
import uk.ac.gda.beamline.i13i.I13IBeamlineActivator;

public class ADControllerImpl implements ADController, InitializingBean {
	private static final Logger logger = LoggerFactory.getLogger(ADControllerImpl.class);

	public NDStats imageNDStats;
	public NDProcess liveViewNDProc;
	private NDArray imageNDArray;
	private int imageHistSize;
	private int imageMin;
	private int imageMax;
	private String detectorName;
	private ADBase adBase;
	private String setExposureTimeCmd;

	private int fFMpegImgWidthRequired;

	private int fFMpegImgHeightRequired;

	private FfmpegStream ffmpegStream;

	private Scannable lensScannable;

	@Override
	public NDStats getImageNDStats() {
		return imageNDStats;
	}

	@Override
	public NDProcess getLiveViewNDProc() {
		return liveViewNDProc;
	}

	public void setLiveViewNDProc(NDProcess ndProc) {
		this.liveViewNDProc = ndProc;
	}

	@Override
	public int getImageHistSize() {
		return imageHistSize;
	}

	@Override
	public int getImageMin() {
		return imageMin;
	}

	@Override
	public int getImageMax() {
		return imageMax;
	}

	@Override
	public String getDetectorName() {
		return detectorName;
	}

	public void setImageNDStats(NDStats ndStats) {
		this.imageNDStats = ndStats;
	}

	public void setImageHistSize(int imageHistSize) {
		this.imageHistSize = imageHistSize;
	}

	public void setImageMin(int imageMin) {
		this.imageMin = imageMin;
	}

	public void setImageMax(int imageMax) {
		this.imageMax = imageMax;
	}

	public void setDetectorName(String detectorName) {
		this.detectorName = detectorName;
	}

	public void setImageNDArray(NDArray imageNDArray) {
		this.imageNDArray = imageNDArray;
	}

	private int[] determineDataDimensions() throws Exception {
		// only called if configured to readArrays (and hence ndArray is set)
		NDPluginBase pluginBase = imageNDArray.getPluginBase();
		int nDimensions = pluginBase.getNDimensions_RBV();
		int[] dimFromEpics = new int[3];
		dimFromEpics[0] = pluginBase.getArraySize2_RBV();
		dimFromEpics[1] = pluginBase.getArraySize1_RBV();
		dimFromEpics[2] = pluginBase.getArraySize0_RBV();

		int[] dims = java.util.Arrays.copyOfRange(dimFromEpics, 3 - nDimensions, 3);
		return dims;
	}

	@Override
	public ImageData getImageData() throws Exception {

		int[] dims = determineDataDimensions();

		int expectedNumPixels = dims[0];
		for (int i = 1; i < dims.length; i++) {
			expectedNumPixels = expectedNumPixels * dims[i];
		}
		Object imageData = imageNDArray.getImageData(expectedNumPixels);
		ImageData data = new ImageData();
		data.dimensions = dims;
		data.data = imageData;
		return data;
	}

	@Override
	public NDArray getImageNDArray() {
		return imageNDArray;
	}

	@Override
	public void setExposure(double d) {
		final String cmd = String.format(getSetExposureTimeCmd(), d);
		InterfaceProvider.getCommandRunner().evaluateCommand(cmd);
	}

	private String getSetExposureTimeCmd() {
		return setExposureTimeCmd;
	}

	public void setSetExposureTimeCmd(String setExposureTimeCmd) {
		this.setExposureTimeCmd = setExposureTimeCmd;
	}

	@Override
	public ADBase getAdBase() {
		return adBase;
	}

	public void setAdBase(ADBase adBase) {
		this.adBase = adBase;
	}

	@Override
	public void afterPropertiesSet() throws Exception {
		if( adBase == null) throw new Exception("adBase is null");
		if (fFMpegImgWidthRequired < 1)
			throw new IllegalArgumentException("fFMpegImgWidthRequired < 1");
		if (fFMpegImgHeightRequired < 1)
			throw new IllegalArgumentException("fFMpegImgHeightRequired < 1");		
		
	}

	@Override
	public void setLiveViewRange(final double range_min, final double range_max) throws Exception {
		//set a monitor on the imageStats array counter, switch on imageStats and histogram if off
		//in monitor remove future updates, return to previous state 
		
		
		final int histSize = getImageHistSize();
		int histMin = getImageMin();
		int histMax = getImageMax();
		getImageNDStats().setHistSize(histSize);
		getImageNDStats().setHistMin(histMin);
		getImageNDStats().setHistMax(histMax);
		double step = (histMax - histMin) / histSize;
		double[] range = new double[histSize];
		range[0] = histMin;
		for (int i = 1; i < histSize; i++) {
			range[i] = range[i - 1] + step;
		}
		final DoubleDataset xData = new DoubleDataset(range);
		
		final boolean wasEnabled = getImageNDStats().getPluginBase().isCallbacksEnabled_RBV();
		final short histogramWasComputed = getImageNDStats().getComputeHistogram_RBV();
		
		final int counterBefore = getImageNDStats().getPluginBase().getArrayCounter_RBV();
		final Observable<Integer> obsvble = getImageNDStats().getPluginBase().createArrayCounterObservable();
		obsvble.addObserver(new Observer<Integer>() {
			
			boolean done=false;
			@Override
			public void update(Observable<Integer> source, Integer arg) {
				if( arg == counterBefore || done)
					return;
				done = true;
				obsvble.deleteIObserver(this);
				try{
					if( histogramWasComputed != 0){
						getImageNDStats().setComputeHistogram(histogramWasComputed);
					}
					if( !wasEnabled){
						getImageNDStats().getPluginBase().disableCallbacks();
					}

					double[] yData = getImageNDStats().getHistogram_RBV(histSize);

					if (yData.length != xData.getSize()) {
						throw new Exception("Length of histogram does not match histSize");
					}
					double min = 0.;
					double max = getImageMax();
					DoubleDataset ds = new DoubleDataset(yData);
					int j = getPosToIncludeFractionOfPopulation(ds, range_max);
					if (j >= 0) {
						max = xData.getDouble(j);
					}
					j = getPosToIncludeFractionOfPopulation(ds, range_min);
					if (j >= 0) {
						min = xData.getDouble(j);
					}
					double offset = -min;
					double scale = 255.0 / (max - min);
					getLiveViewNDProc().setScale(scale);
					getLiveViewNDProc().setOffset(offset);
					getLiveViewNDProc().setEnableOffsetScale(1);
				} catch (Exception e){
					logger.error("Error autoscaling the live view",e);
				}
				
			}
			private int getPosToIncludeFractionOfPopulation(DoubleDataset yData, Double fractionOfPopulationToInclude) {
				Double sum = (Double) yData.sum();
				double[] data = yData.getData();
				int popIncluded = 0;
				int j=0;
				double popRequired = sum * fractionOfPopulationToInclude;
				while (popIncluded < popRequired && j < data.length) {
					popIncluded += data[j];
					if( popIncluded < popRequired)
						j++;
				}
				return Math.min(j, data.length-1);
			}
		});
		
		if( histogramWasComputed != 0){
			getImageNDStats().setComputeHistogram(1);
		}
		if( !wasEnabled){
			getImageNDStats().getPluginBase().enableCallbacks();
		}

		
	}

	@Override
	public FfmpegStream getFfmpegStream() {
		return ffmpegStream;
	}

	public void setFfmpegStream(FfmpegStream ffmpegStream) {
		this.ffmpegStream = ffmpegStream;
	}

	@Override
	public int getfFMpegImgWidthRequired() {
		return fFMpegImgWidthRequired;
	}

	public void setfFMpegImgWidthRequired(int fFMpegImgWidthRequired) {
		this.fFMpegImgWidthRequired = fFMpegImgWidthRequired;
	}

	@Override
	public int getfFMpegImgHeightRequired() {
		return fFMpegImgHeightRequired;
	}

	public void setfFMpegImgHeightRequired(int fFMpegImgHeightRequired) {
		this.fFMpegImgHeightRequired = fFMpegImgHeightRequired;
	}

	@Override
	public void startFfmpegStream() throws Exception {
		FfmpegStream ffmpegStream = getFfmpegStream();
		NDProcess ndProcess = getLiveViewNDProc();
		if (ndProcess.getEnableOffsetScale_RBV() != 1)
			ndProcess.setEnableOffsetScale(1);
		if (ndProcess.getDataTypeOut_RBV() != NDProcess.DatatypeOut_UInt8)
			ndProcess.setDataTypeOut(NDProcess.DatatypeOut_UInt8);

		ndProcess.setEnableHighClip(1);
		ndProcess.setEnableLowClip(1);
		ndProcess.setHighClip(255);
		ndProcess.setLowClip(0);
		NDPluginBase procBase = ndProcess.getPluginBase();
		if (!procBase.isCallbacksEnabled_RBV())
			procBase.enableCallbacks();

		ffmpegStream.setMAXW(getfFMpegImgWidthRequired());
		ffmpegStream.setMAXH(getfFMpegImgHeightRequired());
		ffmpegStream.setQUALITY(100.);
		NDPluginBase ffmpegBase = ffmpegStream.getPluginBase();
		String procPortName_RBV = procBase.getPortName_RBV();
		String ndArrayPort_RBV = ffmpegBase.getNDArrayPort_RBV();
		if (ndArrayPort_RBV == null || !ndArrayPort_RBV.equals(procPortName_RBV))
			ffmpegBase.setNDArrayPort(procPortName_RBV);
		if (!ffmpegBase.isCallbacksEnabled_RBV())
			ffmpegBase.enableCallbacks();

		NDPluginBase arrayBase = getImageNDArray().getPluginBase();
		String procNdArrayPort_RBV = procBase.getNDArrayPort_RBV();
		String ndArrayPort_RBV2 = arrayBase.getNDArrayPort_RBV();
		if (ndArrayPort_RBV2 == null || !ndArrayPort_RBV2.equals(procNdArrayPort_RBV))
			arrayBase.setNDArrayPort(procNdArrayPort_RBV);
		if (!arrayBase.isCallbacksEnabled_RBV())
			arrayBase.enableCallbacks();		
	}

	@Override
	public void stopFfmpegStream() throws Exception {
		NDProcess ndProcess = getLiveViewNDProc();
		NDPluginBase procBase = ndProcess.getPluginBase();
		if (procBase.isCallbacksEnabled_RBV())
			procBase.disableCallbacks();
		
		FfmpegStream ffmpegStream = getFfmpegStream();
		NDPluginBase ffmpegBase = ffmpegStream.getPluginBase();
		if (ffmpegBase.isCallbacksEnabled_RBV())
			ffmpegBase.disableCallbacks();
	}

	public Scannable getLensScannable() {
		return lensScannable;
	}

	public void setLensScannable(Scannable lensScannable) {
		this.lensScannable = lensScannable;
	}





}
