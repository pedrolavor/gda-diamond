/*-
 * Copyright © 2014 Diamond Light Source Ltd.
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

package uk.ac.gda.beamline.i05.views;

import gda.device.DeviceException;
import gda.device.MotorStatus;
import gda.device.Scannable;
import gda.device.scannable.ScannableBase;
import gda.factory.FactoryException;
import gda.factory.Finder;
import gda.jython.InterfaceProvider;
import gda.jython.JythonServerFacade;
import gda.observable.IObserver;
import gda.rcp.views.NudgePositionerComposite;

import java.util.Comparator;
import java.util.Map;
import java.util.TreeMap;

import org.eclipse.swt.SWT;
import org.eclipse.swt.events.SelectionEvent;
import org.eclipse.swt.events.SelectionListener;
import org.eclipse.swt.layout.GridData;
import org.eclipse.swt.layout.GridLayout;
import org.eclipse.swt.widgets.Button;
import org.eclipse.swt.widgets.Combo;
import org.eclipse.swt.widgets.Composite;
import org.eclipse.swt.widgets.Display;
import org.eclipse.swt.widgets.Label;
import org.eclipse.swt.widgets.Text;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import uk.ac.gda.beamline.i05.I05BeamlineActivator;
import uk.ac.gda.devices.vgscienta.AnalyserCapabilties;

import org.eclipse.wb.swt.SWTResourceManager;

public class ContinuousModeControllerComposite{
	
	private static final Logger logger = LoggerFactory.getLogger(ContinuousModeControllerComposite.class);
	private Combo lensMode;
	private Combo passEnergy;
	private Text psuEnergy;	
	private Button startButton;
	private Button stopButton;
	private Button zeroButton;
	private boolean running = false;
	private Button shutterButton;
	
	public ContinuousModeControllerComposite(Composite parent, AnalyserCapabilties capabilities) {
		
		Composite comp = new Composite(parent, SWT.NONE);
		comp.setLayout(new GridLayout(3, true));
		comp.setLayoutData(new GridData(SWT.LEFT, SWT.TOP, false, false, 1, 1));
		
		Composite composite = new Composite(comp, SWT.NONE);
		composite.setLayout(new GridLayout(3, false));
		composite.setLayoutData(new GridData(SWT.LEFT, SWT.CENTER, false, false, 1, 2));
		
		Label label = new Label(composite, SWT.NONE);
		label.setText("lensMode");
		
		lensMode = new Combo(composite, SWT.NONE);
		lensMode.setLayoutData(new GridData(SWT.LEFT, SWT.CENTER, false, false, 2, 1));
		lensMode.setItems(capabilities.getLensModes());
		
		String activeLensMode = JythonServerFacade.getInstance().evaluateCommand("analyser.getLensMode()");
		lensMode.select(comboForMode(activeLensMode, capabilities.getLensModes()));
		SelectionListener lensModeListener = new SelectionListener() {
			@Override
			public void widgetSelected(SelectionEvent e) {
				JythonServerFacade.getInstance().runCommand(String.format("analyser.setLensMode(\"%s\")", lensMode.getItems()[lensMode.getSelectionIndex()] ));
			}
			@Override
			public void widgetDefaultSelected(SelectionEvent e) {
			}
		};
		lensMode.addSelectionListener(lensModeListener);
		
		Comparator<String> passEComparator = new Comparator<String>() {
			@Override
			public int compare(String o1, String o2) {
				return Integer.valueOf(o1.substring(0, o1.lastIndexOf(" "))).compareTo(Integer.valueOf(o2.substring(0, o2.lastIndexOf(" "))));
			}
		};
		final Map<String, Short> passMap = 	new TreeMap<String, Short>(passEComparator);
		for (short s: capabilities.getPassEnergies()) {
			passMap.put(String.format("%d eV", s), s);
		}
		label = new Label(composite, SWT.NONE);
		label.setLayoutData(new GridData(SWT.RIGHT, SWT.CENTER, false, false, 1, 1));
		label.setText("passEnergy");
		
		passEnergy = new Combo(composite, SWT.NONE);
		passEnergy.setLayoutData(new GridData(SWT.FILL, SWT.CENTER, true, false, 2, 1));
		String[] passArray = passMap.keySet().toArray(new String[] {});
		passEnergy.setItems(passArray);
		String activePE = JythonServerFacade.getInstance().evaluateCommand("analyser.getPassEnergy()");
		passEnergy.select(comboForPE(activePE, passArray));
		
		SelectionListener passEnergyListener = new SelectionListener() {
			@Override
			public void widgetSelected(SelectionEvent e) {
				JythonServerFacade.getInstance().runCommand(String.format("analyser.setPassEnergy(%d)", passMap.get(passEnergy.getItem(passEnergy.getSelectionIndex()))));
			}
			@Override
			public void widgetDefaultSelected(SelectionEvent e) {
			}
		};
		passEnergy.addSelectionListener(passEnergyListener);

		label = new Label(composite, SWT.NONE);
		label.setLayoutData(new GridData(SWT.RIGHT, SWT.CENTER, false, false, 1, 1));
		label.setText("psu mode");
		
		psuEnergy = new Text(composite, SWT.BORDER | SWT.LEFT);
		psuEnergy.setEditable(false);

		psuEnergy.setEnabled(false);		
		psuEnergy.setLayoutData(new GridData(SWT.FILL, SWT.CENTER, true, false, 2, 1));
		String psuState = JythonServerFacade.getInstance().evaluateCommand("psu_mode.getPosition()");
		psuEnergy.setText(psuState);
		
		Composite control = new Composite(comp, SWT.NONE);
		control.setLayout(new GridLayout(2, false));
		control.setLayoutData(new GridData(SWT.CENTER, SWT.CENTER, true, false, 1, 2));
		
		startButton = new Button(control, SWT.NONE);
		startButton.setLayoutData(new GridData(SWT.LEFT, SWT.CENTER, true, false, 1, 1));
		startButton.setText("Start");
		SelectionListener startListener = new SelectionListener() {
			@Override
			public void widgetSelected(SelectionEvent e) {
				JythonServerFacade.getInstance().runCommand("am.start()");
			}
			@Override
			public void widgetDefaultSelected(SelectionEvent e) {
			}
		};
		startButton.addSelectionListener(startListener);
		
		stopButton = new Button(control, SWT.NONE);
		stopButton.setLayoutData(new GridData(SWT.RIGHT, SWT.CENTER, true, false, 1, 1));
		stopButton.setText("Stop");
		SelectionListener stopListener = new SelectionListener() {
			@Override
			public void widgetSelected(SelectionEvent e) {
				//am stands for ArpesMonitor. So this stops the ARPES monitor.
				JythonServerFacade.getInstance().runCommand("am.stop()");
			}
			@Override
			public void widgetDefaultSelected(SelectionEvent e) {
			}
		};
		stopButton.addSelectionListener(stopListener);
		
		zeroButton = new Button(control, SWT.NONE);
		zeroButton.setLayoutData(new GridData(SWT.CENTER, SWT.CENTER, true, false, 2, 1));
		zeroButton.setText("Zero Supplies");
		zeroButton.setEnabled(true);
		SelectionListener zeroListener = new SelectionListener() {
			@Override
			public void widgetSelected(SelectionEvent e) {
				// It is important to make sure the analyser is idle before zeroing supplies.
				
				JythonServerFacade.getInstance().runCommand("analyser.getADBase().stopAcquiring()");
				//Sleep as there is a possible race condition between stopping acquisition and zeroing suppies.
				try {
					Thread.sleep(250);
				} catch (InterruptedException e1) {
					logger.error("Error sleeping.", e1);
				};
				JythonServerFacade.getInstance().runCommand("analyser.zeroSupplies()");
			}
			@Override
			public void widgetDefaultSelected(SelectionEvent e) {
			}
		};
		zeroButton.addSelectionListener(zeroListener);
		
		shutterButton = new Button(control, SWT.NONE);
		shutterButton.setForeground(SWTResourceManager.getColor(SWT.COLOR_RED));
		shutterButton.setLayoutData(new GridData(SWT.CENTER, SWT.CENTER, true, false, 2, 1));
		shutterButton.setText("Close Shutter");
		shutterButton.setEnabled(true);
		SelectionListener shutterListener = new SelectionListener() {
			@Override
			public void widgetSelected(SelectionEvent e) {
				//TODO close shutter
				//Shutter 1 (HR line)
				//BL05I-PS-SHTR-01
				//JythonServerFacade.getInstance().runCommand("");
				InterfaceProvider.getCommandRunner().runCommand("hr_shutter(1)");
			}
			@Override
			public void widgetDefaultSelected(SelectionEvent e) {
			}
		};
		shutterButton.addSelectionListener(shutterListener);
		
		ScannableBase wrappedEnergyScannable = new ScannableBase() {
			private Scannable pgmEnergy = (Scannable) (Finder.getInstance().find("pgm_energy"));
			private Scannable combinedEnergy = (Scannable) (Finder.getInstance().find("energy"));

			@Override
			public void configure() throws FactoryException {
				super.configure();
				final ScannableBase we = this;
				pgmEnergy.addIObserver(new IObserver() {
					
					@Override
					public void update(Object source, Object arg) {
						we.notifyIObservers(we, arg);
					}
				});
			}

			@Override
			public boolean isBusy() throws DeviceException {
				return combinedEnergy.isBusy();
			}

			@Override
			public void asynchronousMoveTo(Object externalPosition) throws DeviceException {
				combinedEnergy.asynchronousMoveTo(externalPosition);
			}

			@Override
			public Object getPosition() throws DeviceException {
				return pgmEnergy.getPosition();
			}
		};
		wrappedEnergyScannable.setName("photonEnergy");
		try {
			wrappedEnergyScannable.configure();
		} catch (FactoryException e) {
			logger.error("error configuring wrapped energy scannable", e);
		}
		
		Composite viewerComposite = new Composite(comp, SWT.NONE);
		viewerComposite.setLayoutData(new GridData(SWT.LEFT, SWT.CENTER, false, false, 2, 1));
		GridLayout glViewerComposite = new GridLayout(2, false);
		glViewerComposite.horizontalSpacing = 25;
		viewerComposite.setLayout(glViewerComposite);
		
		Composite comp1 = new Composite(viewerComposite, SWT.NONE);
		viewerComposite.setLayoutData(new GridData(SWT.LEFT, SWT.CENTER, false, false, 2, 1));
		GridLayout glcomp1 = new GridLayout(3, false);
		glcomp1.horizontalSpacing = 25;
		comp1.setLayout(glcomp1);
		
		new NudgePositionerComposite(comp1, SWT.RIGHT, (Scannable) (Finder.getInstance().find("acquire_time")), true, null, true, true);
		new NudgePositionerComposite(comp1, SWT.RIGHT, wrappedEnergyScannable, true, null, true, true);
		new Label(comp1, SWT.NONE);
		
		new NudgePositionerComposite(comp1, SWT.RIGHT, (Scannable) (Finder.getInstance().find(I05BeamlineActivator.EXIT_SLIT_SIZE_SCANNABLE)), true, "exitSlit", true, true);
		new NudgePositionerComposite(comp1, SWT.RIGHT, (Scannable) (Finder.getInstance().find("s2_ysize")), true, null, true, true);
		new NudgePositionerComposite(comp1, SWT.RIGHT, (Scannable) (Finder.getInstance().find("s2_xsize")), true, null, true, true);
		
		
		new NudgePositionerComposite(viewerComposite, SWT.RIGHT, (Scannable) (Finder.getInstance().find("raw_centre_energy")), true, "centre_energy", false, true);
		
		Composite nudgeComposite = new Composite(viewerComposite, SWT.NONE);
		nudgeComposite.setLayoutData(new GridData(SWT.LEFT, SWT.CENTER, false, false, 3, 1));
		GridLayout glNudgeComposite = new GridLayout(3, false);
		glNudgeComposite.horizontalSpacing = 25;
		nudgeComposite.setLayout(glNudgeComposite);
		
		
		new NudgePositionerComposite(nudgeComposite, SWT.RIGHT, (Scannable)(Finder.getInstance().find("sax")));
		new NudgePositionerComposite(nudgeComposite, SWT.RIGHT, (Scannable)(Finder.getInstance().find("say")));
		new NudgePositionerComposite(nudgeComposite, SWT.RIGHT, (Scannable)(Finder.getInstance().find("saz")));
		new NudgePositionerComposite(nudgeComposite, SWT.RIGHT, (Scannable)(Finder.getInstance().find("satilt")));
		new NudgePositionerComposite(nudgeComposite, SWT.RIGHT, (Scannable)(Finder.getInstance().find("sapolar")));
		new NudgePositionerComposite(nudgeComposite, SWT.RIGHT, (Scannable)(Finder.getInstance().find("saazimuth")));
		new Label(nudgeComposite, SWT.NONE);
		new Label(nudgeComposite, SWT.NONE);
		new Label(comp, SWT.NONE);
	}
	
	private int comboForPE(String pe, String[] passArray) {
		pe = pe + " eV";
		for (int i = 0; i < passArray.length; i++) {
			if (passArray[i].equals(pe))
				return i;
		} 
		return -1;
	}
	
	private int comboForMode(String mode, String[] lensModes) {
		for (int i = 0; i < lensModes.length; i++) {
			if (lensModes[i].equals(mode))
				return i;
		} 
		return -1;
	}
	
	public void update(Object arg){
		if (arg instanceof MotorStatus) {
			running = MotorStatus.BUSY.equals(arg);
			Display.getDefault().asyncExec(new Runnable() {
				@Override
				public void run() {
					startButton.setEnabled(!running);
					startButton.setSelection(running);
					stopButton.setEnabled(running);
					stopButton.setSelection(!running);
				}
			});
		}
	}
	
	public Button getStartButton(){
		return startButton;
	}

}
