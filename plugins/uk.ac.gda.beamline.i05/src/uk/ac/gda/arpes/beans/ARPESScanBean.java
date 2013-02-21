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

package uk.ac.gda.arpes.beans;

import java.net.URL;

import uk.ac.gda.beans.IRichBean;
import uk.ac.gda.util.beans.xml.XMLHelpers;

public class ARPESScanBean implements IRichBean {

	static public final URL mappingURL = ARPESScanBean.class.getResource("ARPESMapping.xml");
	static public final URL schemaURL  = ARPESScanBean.class.getResource("ARPESMapping.xsd");

	String lensMode;
	short passEnergy;
	double photonEnergy;
	double startEnergy, endEnergy, stepEnergy;
	double timePerStep;
	short iterations;
	double sampleTemperature;
	boolean sweptMode;
	
	public static ARPESScanBean createFromXML(String filename) throws Exception {
		return (ARPESScanBean) XMLHelpers.createFromXML(mappingURL, ARPESScanBean.class, schemaURL, filename);
	}
	
	public static void writeToXML(ARPESScanBean bean, String filename) throws Exception {
		XMLHelpers.writeToXML(mappingURL, bean, filename);
	}

	@Override
	public void clear() {
		// TODO
	}

	public String getLensMode() {
		return lensMode;
	}

	public void setLensMode(String lensMode) {
		this.lensMode = lensMode;
	}

	public short getPassEnergy() {
		return passEnergy;
	}

	public void setPassEnergy(short passEnergy) {
		this.passEnergy = passEnergy;
	}

	public double getPhotonEnergy() {
		return photonEnergy;
	}

	public void setPhotonEnergy(double photonEnergy) {
		this.photonEnergy = photonEnergy;
	}

	public double getStartEnergy() {
		return startEnergy;
	}

	public void setStartEnergy(double startEnergy) {
		this.startEnergy = startEnergy;
	}

	public double getEndEnergy() {
		return endEnergy;
	}

	public void setEndEnergy(double endEnergy) {
		this.endEnergy = endEnergy;
	}

	public double getStepEnergy() {
		return stepEnergy;
	}

	public void setStepEnergy(double stepEnergy) {
		this.stepEnergy = stepEnergy;
	}

	public double getTimePerStep() {
		return timePerStep;
	}

	public void setTimePerStep(double timePerStep) {
		this.timePerStep = timePerStep;
	}

	public short getIterations() {
		return iterations;
	}

	public void setIterations(short iterations) {
		this.iterations = iterations;
	}

	public double getSampleTemperature() {
		return sampleTemperature;
	}

	public void setSampleTemperature(double sampleTemperature) {
		this.sampleTemperature = sampleTemperature;
	}

	public boolean isSweptMode() {
		return sweptMode;
	}

	public void setSweptMode(boolean sweptMode) {
		this.sweptMode = sweptMode;
	}
}