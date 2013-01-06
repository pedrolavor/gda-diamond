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

package uk.ac.gda.beamline.i13i.views.adScaleAdjustmentView;

import org.eclipse.core.runtime.CoreException;
import org.eclipse.core.runtime.IConfigurationElement;
import org.eclipse.core.runtime.IExecutableExtension;
import org.eclipse.core.runtime.IExecutableExtensionFactory;
import org.eclipse.core.runtime.IStatus;
import org.eclipse.core.runtime.Status;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import uk.ac.gda.beamline.i13i.I13IBeamlineActivator;

public abstract class AreaDetectorViewCreatorBase implements IExecutableExtensionFactory, IExecutableExtension{

	public AreaDetectorViewCreatorBase() {
		super();
	}
	private static final Logger logger = LoggerFactory.getLogger(AreaDetectorLiveViewCreator.class);
	
	@Override
	public Object create() throws CoreException {
		Object namedService = I13IBeamlineActivator.getNamedService(ADViewCreator.class, serviceName);
		ADViewCreator adController = (ADViewCreator) namedService;
		try {
			return getView(adController);
		} catch (Exception e) {
			logger.error("Error creating view ", e);
			throw new CoreException(new Status(IStatus.ERROR, I13IBeamlineActivator.PLUGIN_ID,
					"Error creating view :'" + e.getMessage() + "'"));
		}		
	}

	String serviceName="";
	@Override
	public void setInitializationData(IConfigurationElement config, String propertyName, Object data)
			throws CoreException {
		if( propertyName.equals("class") && data instanceof String){
			serviceName = (String)data;
		}

	}
	
	abstract protected Object getView(ADViewCreator adController);


}