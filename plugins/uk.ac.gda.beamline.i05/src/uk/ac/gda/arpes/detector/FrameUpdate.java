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

package uk.ac.gda.arpes.detector;

import java.io.Serializable;

public class FrameUpdate implements Serializable {
	
	public static final long serialVersionUID = 1L;
	
	public int mFrame, cFrame;
	public FrameUpdate() { }
	public FrameUpdate(int c, int m) {
		mFrame = m;
		cFrame = c;
	}
	public int getMaxFrame() {
		return mFrame;
	}
	public int getCurrentFrame() {
		return cFrame;
	}
}