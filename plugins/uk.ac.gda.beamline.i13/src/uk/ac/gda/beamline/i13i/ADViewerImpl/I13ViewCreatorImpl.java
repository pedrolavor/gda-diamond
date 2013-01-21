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

import uk.ac.gda.epics.adviewer.views.ViewCreatorImpl;

public class I13ViewCreatorImpl extends ViewCreatorImpl {

	
	@Override
	public Object createLiveView() {
		return new I13MJPegView((I13ADControllerImpl)adController);
	}

	@Override
	public void afterPropertiesSet() throws Exception {
		super.afterPropertiesSet();
		if( ! (adController instanceof I13ADControllerImpl) )
			throw new Exception("adController is not of type I13ADControllerImpl");
	}


}

