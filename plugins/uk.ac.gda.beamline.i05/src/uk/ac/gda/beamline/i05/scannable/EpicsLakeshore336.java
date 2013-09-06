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

package uk.ac.gda.beamline.i05.scannable;

import gda.device.DeviceException;
import gda.device.detector.areadetector.IPVProvider;
import gda.device.scannable.ScannableBase;
import gda.device.scannable.ScannableUtils;
import gda.epics.connection.EpicsController;
import gda.factory.FactoryException;
import gov.aps.jca.Channel;

import java.util.HashMap;
import java.util.Map;

public class EpicsLakeshore336 extends ScannableBase {

	private final EpicsController EPICS_CONTROLLER = EpicsController.getInstance();
	private String basePVName = null;
	private IPVProvider pvProvider;
	
	public static final String CH_TEMP = "KRDG%d";
	public static final String CH0TEMP = "KRDG0";
	public static final String CH1TEMP = "KRDG1";
	public static final String CH2TEMP = "KRDG2";
	public static final String CH3TEMP = "KRDG3";
	
	public static final String LOOP_DEMAND = "SETP_S%d";
	public static final String LOOP_DEMAND_RBV = "SETP%d";
	public static final String LOOP_OUTPUT = "HTR%d";
	public static final String LOOP_HEATERRANGE = "RANGE_S%d";
	public static final String LOOP_HEATERRANGE_RBV = "RANGE_S%d";
	public static final String LOOP_RATE = "RAMP_S%d";
	public static final String LOOP_RATE_RBV = "RAMP%d";
	public static final String LOOP_INPUT = "OMINPUT_S%d";
	public static final String LOOP_INPUT_RBV = "OMINPUT%d";

	double tolerance = 0.01;
	
	/**
	 * Map that stores the channel against the PV name
	 */
	private Map<String, Channel> channelMap = new HashMap<String, Channel>();
	
	private Channel getChannel(String pvPostFix, int number) throws Exception {
		return getChannel(String.format(pvPostFix, number));
	}
	
	private Channel getChannel(String pvPostFix) throws Exception {
		String fullPvName;
		if (pvProvider != null) {
			fullPvName = pvProvider.getPV(pvPostFix);
		} else {
			fullPvName = basePVName + pvPostFix;
		}
		Channel channel = channelMap.get(fullPvName);
		if (channel == null) {
			channel = EPICS_CONTROLLER.createChannel(fullPvName);
			channelMap.put(fullPvName, channel);
		}
		return channel;
	}

	public IPVProvider getPvProvider() {
		return pvProvider;
	}

	public void setPvProvider(IPVProvider pvProvider) {
		this.pvProvider = pvProvider;
	}

	public String getBasePVName() {
		return basePVName;
	}

	public void setBasePVName(String basePVName) {
		this.basePVName = basePVName;
	}

	@Override
	public void configure() throws FactoryException {
		super.configure();
		
		setInputNames(new String[] {"demand"});
		setExtraNames(new String[] {"ch0", "ch1", "ch2", "ch3", "heater"});
	}
	/**
	 * We assume the PID control tuned reasonably well so we don't have to deal with overshooting or ringing 
	 */
	@Override
	public boolean isBusy() throws DeviceException {
		if (getActiveLoop() == 0)
			return false;
		return Math.abs(getDemandTemperature()-getControlledTemperature()) > tolerance;
	}

	@Override
	public Double[] getPosition() throws DeviceException {
		Double[] pos = new Double[] { 
				getDemandTemperature(),
				getTemperature(0),
				getTemperature(1),
				getTemperature(2),
				getTemperature(3),
				getHeaterPercent()
		};
		return pos;
	}

	@Override
	public void asynchronousMoveTo(Object externalPosition) throws DeviceException {
		int activeLoop = getActiveLoop();
		if (activeLoop == 0)
			throw new DeviceException("no control loop currently active on this device and I am not allowed to enable one yet.");
		Double[] doubles = ScannableUtils.objectToArray(externalPosition);
		setDemandTemperature(doubles[0]);
	}
	
	private Double getHeaterPercent() throws DeviceException {
		try {
			if (getActiveLoop() == 0)
				return 0.0;
			return EPICS_CONTROLLER.cagetDouble(getChannel(LOOP_OUTPUT, getActiveLoop()));
		} catch (Exception e) {
			throw new DeviceException("error reading from lakeshore device", e);
		}
	}

	private Double getTemperature(int i) throws DeviceException {
		try {
			return EPICS_CONTROLLER.cagetDouble(getChannel(CH_TEMP, i));
		} catch (Exception e) {
			throw new DeviceException("error reading from lakeshore device", e);
		}
	}

	public Double getControlledTemperature() throws DeviceException {
		try {
			if (getActiveLoop() == 0)
				return null;
			int sensor = EPICS_CONTROLLER.cagetInt(getChannel(LOOP_INPUT_RBV, getActiveLoop())) - 1;
			return EPICS_CONTROLLER.cagetDouble(getChannel(CH_TEMP, sensor));
		} catch (Exception e) {
			throw new DeviceException("error reading from lakeshore device", e);
		}
	}

	public void setDemandTemperature(double demand) throws DeviceException {
		try {
			if (getActiveLoop() == 0)
				return;
			EPICS_CONTROLLER.caput(getChannel(LOOP_DEMAND, getActiveLoop()), demand);
		} catch (Exception e) {
			throw new DeviceException("error setting value in lakeshore device", e);
		}	
	}
	
	public Double getDemandTemperature() throws DeviceException {
		try {
			if (getActiveLoop() == 0)
				return null;
			return EPICS_CONTROLLER.cagetDouble(getChannel(LOOP_DEMAND_RBV, getActiveLoop()));
		} catch (Exception e) {
			throw new DeviceException("error reading from lakeshore device", e);
		}	
	}

	public int getActiveLoop() throws DeviceException {
		try {
			for(int i: new int[] {1, 2}) {
			if (EPICS_CONTROLLER.cagetInt(getChannel(LOOP_HEATERRANGE,i)) != 0)
				return i;
			}
		} catch (Exception e) {
			throw new DeviceException("error reading from lakeshore device", e);
		}
		return 0;
	}
}