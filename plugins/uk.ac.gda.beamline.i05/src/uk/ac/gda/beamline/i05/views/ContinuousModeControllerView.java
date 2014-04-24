package uk.ac.gda.beamline.i05.views;

import gda.device.Device;
import gda.factory.Finder;
import gda.observable.IObserver;

import org.eclipse.swt.widgets.Composite;
import org.eclipse.ui.part.ViewPart;

import uk.ac.gda.devices.vgscienta.AnalyserCapabilties;

public class ContinuousModeControllerView extends ViewPart implements IObserver {
	
	private Device analyser;
	private AnalyserCapabilties capabilities;
	
	public ContinuousModeControllerView() {
	}

	private ContinuousModeControllerComposite continuousModeControllerComposite;
	
	@Override
	public void createPartControl(Composite parent) {	
		capabilities = (AnalyserCapabilties) Finder.getInstance().listAllLocalObjects(AnalyserCapabilties.class.getCanonicalName()).get(0);
		analyser = (Device) Finder.getInstance().find("analyser");
		if (analyser != null) {
			analyser.addIObserver(this);
		}
		continuousModeControllerComposite = new ContinuousModeControllerComposite(parent, capabilities);
	}

	@Override
	public void setFocus() {
	}

	@Override
	public void update(Object source, Object arg) {
		if (continuousModeControllerComposite.getStartButton().isDisposed()) {
			analyser.deleteIObserver(this);
			return;
		}
		continuousModeControllerComposite.update(arg);
	}
}