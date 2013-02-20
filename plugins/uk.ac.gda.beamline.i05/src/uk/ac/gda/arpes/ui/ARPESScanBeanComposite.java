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

package uk.ac.gda.arpes.ui;

import gda.commandqueue.JythonCommandCommandProvider;
import gda.commandqueue.Queue;

import java.util.Comparator;
import java.util.Map;
import java.util.TreeMap;

import org.eclipse.core.runtime.IProgressMonitor;
import org.eclipse.core.runtime.NullProgressMonitor;
import org.eclipse.swt.SWT;
import org.eclipse.swt.events.ExpandAdapter;
import org.eclipse.swt.events.ExpandEvent;
import org.eclipse.swt.events.SelectionAdapter;
import org.eclipse.swt.events.SelectionEvent;
import org.eclipse.swt.layout.GridData;
import org.eclipse.swt.layout.GridLayout;
import org.eclipse.swt.widgets.Button;
import org.eclipse.swt.widgets.Composite;
import org.eclipse.swt.widgets.Display;
import org.eclipse.swt.widgets.ExpandBar;
import org.eclipse.swt.widgets.ExpandItem;
import org.eclipse.swt.widgets.Label;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import uk.ac.gda.arpes.detector.AnalyserCapabilties;
import uk.ac.gda.client.CommandQueueViewFactory;
import uk.ac.gda.richbeans.ACTIVE_MODE;
import uk.ac.gda.richbeans.beans.IFieldWidget;
import uk.ac.gda.richbeans.components.FieldComposite;
import uk.ac.gda.richbeans.components.scalebox.IntegerBox;
import uk.ac.gda.richbeans.components.scalebox.NumberBox;
import uk.ac.gda.richbeans.components.scalebox.ScaleBox;
import uk.ac.gda.richbeans.components.wrappers.ComboWrapper;
import uk.ac.gda.richbeans.components.wrappers.RadioWrapper;
import uk.ac.gda.richbeans.components.wrappers.TextWrapper;
import uk.ac.gda.richbeans.editors.RichBeanEditorPart;
import uk.ac.gda.richbeans.event.ValueEvent;
import uk.ac.gda.richbeans.event.ValueListener;

public final class ARPESScanBeanComposite extends Composite implements ValueListener {
	private static final Logger logger = LoggerFactory.getLogger(ARPESScanBeanComposite.class);
	
	private final ComboWrapper lensMode;
	private final ComboWrapper passEnergy;
	private final NumberBox photonEnergy;
	private final NumberBox startEnergy;
	private final NumberBox endEnergy;
	private final NumberBox stepEnergy;
	private final NumberBox timePerStep;
	private final NumberBox iterations;
	private final NumberBox sampleTemperature;
	private final RadioWrapper sweptMode;
	private final ScaleBox centreEnergy;
	private final ScaleBox energyWidth;

	private AnalyserCapabilties capabilities;

	public ARPESScanBeanComposite(final Composite parent, int style, final RichBeanEditorPart editor) {
		super(parent, style);
		setLayout(new GridLayout(2, false));

		capabilities = new AnalyserCapabilties();
		
		Label label = new Label(this, SWT.NONE);
		label.setLayoutData(new GridData(SWT.RIGHT, SWT.CENTER, false, false, 1, 1));
		
		Button btnQueueExperiment = new Button(this, SWT.NONE);
		GridData layoutData = new GridData(SWT.RIGHT, SWT.CENTER, true, false, 1, 1);
		btnQueueExperiment.setLayoutData(layoutData);
		btnQueueExperiment.setText("Queue Experiment");
		btnQueueExperiment.setToolTipText("save file and queue for execution (will start immediately if queue running");
		btnQueueExperiment.addSelectionListener(new SelectionAdapter() {

			@Override
			public void widgetSelected(SelectionEvent e) {
				super.widgetSelected(e);
				try {
					IProgressMonitor monitor = new NullProgressMonitor();
					editor.doSave(monitor);
					if (monitor.isCanceled())
						return;
					Queue queue = CommandQueueViewFactory.getQueue();
					if (queue != null) {
						queue.addToTail(new JythonCommandCommandProvider(String.format("import arpes; arpes.APRESRun(\"%s\").run()", editor.getPath()), editor.getTitle(), editor.getPath()));
					} else {
						logger.warn("No queue received from CommandQueueViewFactory");
					}
				} catch (Exception e1) {
					logger.error("Error adding command to the queue", e1);
				}
			}
		});

		label = new Label(this, SWT.NONE);
		label.setLayoutData(new GridData(SWT.RIGHT, SWT.CENTER, false, false, 1, 1));
		label.setText("lensMode");
		this.lensMode = new ComboWrapper(this, SWT.NONE);
		this.lensMode.setItems(new String[] {"Transmission", "Angular7", "Angular7_fix", "Angular14", "A14small", "Angular30", "A30small"});
		lensMode.setLayoutData(new GridData(SWT.FILL, SWT.CENTER, true, false, 1, 1));

		Comparator<String> passEComparator = new Comparator<String>() {
			@Override
			public int compare(String o1, String o2) {
				return Integer.valueOf(o1.substring(0, o1.lastIndexOf(" "))).compareTo(Integer.valueOf(o2.substring(0, o2.lastIndexOf(" "))));
			}
		};
		Map<String, Short> passMap = 	new TreeMap<String, Short>(passEComparator) {{
			put("1 eV", (short) 1);
			put("2 eV", (short) 2);
			put("5 eV", (short) 5);
			put("10 eV", (short) 10);
			put("20 eV", (short) 20);
			put("50 eV", (short) 50);
			put("100 eV", (short) 100);
			put("200 eV", (short) 200);
			put("500 eV", (short) 500);
		}};
		label = new Label(this, SWT.NONE);
		label.setLayoutData(new GridData(SWT.RIGHT, SWT.CENTER, false, false, 1, 1));
		label.setText("passEnergy");
		this.passEnergy = new ComboWrapper(this, SWT.NONE);
		this.passEnergy.setItems(passMap);
		this.passEnergy.addValueListener(this);
		passEnergy.setLayoutData(new GridData(SWT.FILL, SWT.CENTER, true, false, 1, 1));

		label = new Label(this, SWT.NONE);
		label.setLayoutData(new GridData(SWT.RIGHT, SWT.CENTER, false, false, 1, 1));
		label.setText("sweptMode");
		this.sweptMode = new RadioWrapper(this, SWT.NONE, new String[] { "fixed", "swept"}) {
			@Override
			public void setValue(Object value) {
				super.setValue((Boolean) value ? "swept" : "fixed");
			}
			@Override
			public Object getValue() {
				return super.getValue().equals("swept");
			}
		};
		sweptMode.setLayoutData(new GridData(SWT.FILL, SWT.CENTER, true, false, 1, 1));
		sweptMode.addValueListener(this);
		
		label = new Label(this, SWT.NONE);
		label.setLayoutData(new GridData(SWT.RIGHT, SWT.CENTER, false, false, 1, 1));
		label.setText("startEnergy");
		this.startEnergy = new ScaleBox(this, SWT.NONE);
		startEnergy.setLayoutData(new GridData(SWT.FILL, SWT.CENTER, true, false, 1, 1));
		startEnergy.setUnit("eV");
		startEnergy.setDecimalPlaces(3);
		startEnergy.addValueListener(this);
		
		label = new Label(this, SWT.NONE);
		label.setLayoutData(new GridData(SWT.RIGHT, SWT.CENTER, false, false, 1, 1));
		label.setText("centreEnergy");
		centreEnergy = new ScaleBox(this, SWT.NONE);
		centreEnergy.setLayoutData(new GridData(SWT.FILL, SWT.CENTER, true, false, 1, 1));
		centreEnergy.setUnit("eV");
		centreEnergy.setDecimalPlaces(3);
		centreEnergy.setFieldName("centreEnergy");
		centreEnergy.on();
		centreEnergy.addValueListener(this);
		
		label = new Label(this, SWT.NONE);
		label.setLayoutData(new GridData(SWT.RIGHT, SWT.CENTER, false, false, 1, 1));
		label.setText("endEnergy");
		this.endEnergy = new ScaleBox(this, SWT.NONE);
		endEnergy.setLayoutData(new GridData(SWT.FILL, SWT.CENTER, true, false, 1, 1));
		endEnergy.setUnit("eV");
		endEnergy.setDecimalPlaces(3);
		endEnergy.addValueListener(this);
		
		label = new Label(this, SWT.NONE);
		label.setLayoutData(new GridData(SWT.RIGHT, SWT.CENTER, false, false, 1, 1));
		label.setText("stepEnergy");
		this.stepEnergy = new ScaleBox(this, SWT.NONE);
		stepEnergy.setLayoutData(new GridData(SWT.FILL, SWT.CENTER, true, false, 1, 1));
		stepEnergy.setUnit("eV");
		stepEnergy.setDecimalPlaces(4);
		stepEnergy.setMaximum(10);
		stepEnergy.setMinimum(0.0001);
		stepEnergy.addValueListener(this);
		
		label = new Label(this, SWT.NONE);
		label.setLayoutData(new GridData(SWT.RIGHT, SWT.CENTER, false, false, 1, 1));
		label.setText("energyWidth");
		energyWidth = new ScaleBox(this, SWT.NONE);
		energyWidth.setLayoutData(new GridData(SWT.FILL, SWT.CENTER, true, false, 1, 1));
		energyWidth.setUnit("eV");
		energyWidth.setDecimalPlaces(3);
		energyWidth.setFieldName("energyWidth");
		energyWidth.on();
		energyWidth.setActiveMode(ACTIVE_MODE.SET_ENABLED_AND_ACTIVE);
		energyWidth.addValueListener(this);
		
		label = new Label(this, SWT.NONE);
		label.setLayoutData(new GridData(SWT.RIGHT, SWT.CENTER, false, false, 1, 1));
		label.setText("timePerStep");
		this.timePerStep = new ScaleBox(this, SWT.NONE);
		timePerStep.setLayoutData(new GridData(SWT.FILL, SWT.CENTER, true, false, 1, 1));
		timePerStep.setUnit("s");
		timePerStep.addValueListener(this);
		
		label = new Label(this, SWT.NONE);
		label.setLayoutData(new GridData(SWT.RIGHT, SWT.CENTER, false, false, 1, 1));
		label.setText("iterations");
		this.iterations = new IntegerBox(this, SWT.NONE);
		iterations.setLayoutData(new GridData(SWT.FILL, SWT.CENTER, true, false, 1, 1));
		iterations.addValueListener(this);
		
		ExpandBar bar = new ExpandBar(this, SWT.V_SCROLL);
		bar.setLayoutData(new GridData(SWT.FILL, SWT.FILL, false, true, 2, 10));

		Composite composite = new Composite (bar, SWT.NONE);
		GridLayout layout = new GridLayout (2, false);
		composite.setLayout(layout);

		label = new Label(composite, SWT.NONE);
		label.setLayoutData(new GridData(SWT.RIGHT, SWT.CENTER, false, false, 1, 1));
		label.setText("photonEnergy");
		this.photonEnergy = new ScaleBox(composite, SWT.NONE);
		photonEnergy.setLayoutData(new GridData(SWT.FILL, SWT.CENTER, true, false, 1, 1));
		photonEnergy.setUnit("eV");
		photonEnergy.setDecimalPlaces(3);
		photonEnergy.addValueListener(this);
		
		ExpandItem item0 = new ExpandItem(bar, SWT.NONE, 0);
		item0.setText("Source");
		item0.setHeight(composite.computeSize(SWT.DEFAULT, SWT.DEFAULT).y);
//		item0.setHeight(200);
		item0.setControl(composite);
		
		composite = new Composite (bar, SWT.NONE);
		layout = new GridLayout (2, false);
		composite.setLayout(layout);
		
		label = new Label(composite, SWT.NONE);
		label.setLayoutData(new GridData(SWT.RIGHT, SWT.CENTER, false, false, 1, 1));
		label.setText("sampleTemperature");
		this.sampleTemperature = new ScaleBox(composite, SWT.NONE);
		sampleTemperature.setLayoutData(new GridData(SWT.FILL, SWT.CENTER, true, false, 1, 1));
		sampleTemperature.setUnit("K");
		sampleTemperature.addValueListener(this);
		
		ExpandItem item1 = new ExpandItem(bar, SWT.NONE, 0);
		item1.setText("Sample");
		item1.setHeight(composite.computeSize(SWT.DEFAULT, SWT.DEFAULT).y);
//		item1.setHeight(100);
		item1.setControl(composite);
		
        bar.addExpandListener(new ExpandAdapter() {
        	 
            @Override
            public void itemCollapsed(ExpandEvent e) {
                Display.getCurrent().asyncExec(new Runnable() {
                    @Override
					public void run() {
                        layout();
                    }
                });
            }
 
            @Override
            public void itemExpanded(ExpandEvent e) {
                Display.getCurrent().asyncExec(new Runnable() {
                    @Override
					public void run() {
                        layout();
                    }
                });
            }
        });
	}

	public FieldComposite getLensMode() {
		return lensMode;
	}

	public FieldComposite getPassEnergy() {
		return passEnergy;
	}

	public FieldComposite getPhotonEnergy() {
		return photonEnergy;
	}

	public FieldComposite getStartEnergy() {
		return startEnergy;
	}

	public FieldComposite getEndEnergy() {
		return endEnergy;
	}

	public FieldComposite getStepEnergy() {
		return stepEnergy;
	}

	public FieldComposite getTimePerStep() {
		return timePerStep;
	}

	public FieldComposite getIterations() {
		return iterations;
	}

	public FieldComposite getSampleTemperature() {
		return sampleTemperature;
	}

	public IFieldWidget getSweptMode() {
		return sweptMode;
	}

	boolean wedidit = false;
	
	private boolean isSwept() {
		return (Boolean) sweptMode.getValue();
	}
	
	@Override
	public void valueChangePerformed(ValueEvent e) {
	
		if (Double.isNaN(e.getDoubleValue())) 
			return; 
		
		if (wedidit) return;
		
		wedidit = true;
		
		try {
			if (e.getFieldName().equals("sweptMode")) {
				stepEnergy.setMinimum(capabilities.getEnergyStepForPass(((Number) passEnergy.getValue()).intValue()));
				if (!isSwept()) {
					stepEnergy.setValue(capabilities.getEnergyStepForPass(((Number) passEnergy.getValue()).intValue()));
					energyWidth.setValue(capabilities.getEnergyWidthForPass(((Number) passEnergy.getValue()).intValue()));
					energyWidth.setActive(false);
					startEnergy.setValue(((Number) centreEnergy.getValue()).doubleValue() - ((Number) energyWidth.getValue()).doubleValue()/2.0);
					endEnergy.setValue(((Number) centreEnergy.getValue()).doubleValue() + ((Number) energyWidth.getValue()).doubleValue()/2.0);

				} else {
					energyWidth.setActive(true);
				}
			}

			if (e.getFieldName().equals("passEnergy") || (e.getFieldName().equals("sweptMode") && (Boolean) e.getValue())) {
				stepEnergy.setMinimum(capabilities.getEnergyStepForPass(((Number) passEnergy.getValue()).intValue()));
				if (!isSwept()) {
					stepEnergy.setValue(capabilities.getEnergyStepForPass(((Number) passEnergy.getValue()).intValue()));

					energyWidth.setValue(capabilities.getEnergyWidthForPass(((Number) passEnergy.getValue()).intValue()));
					startEnergy.setValue(((Number) centreEnergy.getValue()).doubleValue() - e.getDoubleValue()/2.0);
					endEnergy.setValue(((Number) centreEnergy.getValue()).doubleValue() + e.getDoubleValue()/2.0);
				}
			}
		
			if (isSwept()) {
				if (e.getFieldName().equals("startEnergy")) {
					centreEnergy.setValue((((Number) endEnergy.getValue()).doubleValue() + e.getDoubleValue())/2.0);
					energyWidth.setValue(((Number) endEnergy.getValue()).doubleValue() - e.getDoubleValue());
				}
				
				if (e.getFieldName().equals("endEnergy")) {
					centreEnergy.setValue((((Number) startEnergy.getValue()).doubleValue() + e.getDoubleValue())/2.0);
					energyWidth.setValue(-1 *((Number) startEnergy.getValue()).doubleValue() + e.getDoubleValue());
				}
				
				if (e.getFieldName().equals("energyWidth")) {
					startEnergy.setValue(((Number) centreEnergy.getValue()).doubleValue() - e.getDoubleValue()/2.0);
					endEnergy.setValue(((Number) centreEnergy.getValue()).doubleValue() + e.getDoubleValue()/2.0);
				}
			} else {
				if (e.getFieldName().equals("startEnergy")) {
					centreEnergy.setValue(((Number) energyWidth.getValue()).doubleValue()/2.0 + e.getDoubleValue());
					endEnergy.setValue(((Number) energyWidth.getValue()).doubleValue() + e.getDoubleValue());
				}
				
				if (e.getFieldName().equals("endEnergy")) {
					centreEnergy.setValue(e.getDoubleValue() - ((Number) energyWidth.getValue()).doubleValue()/2.0);
					startEnergy.setValue(e.getDoubleValue() - ((Number) energyWidth.getValue()).doubleValue());
				}
				
				if (e.getFieldName().equals("energyWidth")) {
					// not allowed
				}
			}

			if (e.getFieldName().equals("centreEnergy")) {
				startEnergy.setValue(e.getDoubleValue() - ((Number) energyWidth.getValue()).doubleValue()/2.0);
				endEnergy.setValue(e.getDoubleValue() + ((Number) energyWidth.getValue()).doubleValue()/2.0);
			}
				
		} finally {
			wedidit = false;
		}
	}

	@Override
	public String getValueListenerName() {
		return null;
	}

	public void beanUpdated() {
		wedidit = true;
		try {
			stepEnergy.setMinimum(capabilities.getEnergyStepForPass(((Number) passEnergy.getValue()).intValue()));
			if (!isSwept()) {
				stepEnergy.setValue(capabilities.getEnergyStepForPass(((Number) passEnergy.getValue()).intValue()));
				energyWidth.setActive(false);
			} else {
				energyWidth.setActive(true);
			}
			centreEnergy.setValue((((Number) endEnergy.getValue()).doubleValue() + ((Number) startEnergy.getValue()).doubleValue())/2.0);
			energyWidth.setValue(((Number) endEnergy.getValue()).doubleValue() - ((Number) startEnergy.getValue()).doubleValue());
		} finally {
			wedidit = false;
		}
	}
}