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

import gda.data.scan.datawriter.SelfCreatingLink;
import gda.data.scan.datawriter.scannablewriter.ComponentWriter;
import gda.data.scan.datawriter.scannablewriter.NumberComponentWriter;
import gda.data.scan.datawriter.scannablewriter.SingleScannableWriter;
import gda.data.scan.datawriter.scannablewriter.StringComponentWriter;

import java.util.Collection;
import java.util.Collections;

import org.apache.commons.lang.ArrayUtils;
import org.nexusformat.NeXusFileInterface;
import org.nexusformat.NexusException;

public class EnergyScannableWriter extends SingleScannableWriter {

	String stokesPath = "instrument:NXinstrument/insertion_device:NXinsertion_device/beam:NXbeam/final_polarisation_stokes";

	protected class DoubleArrayComponentWriter extends NumberComponentWriter {
		final int arraylength;

		public DoubleArrayComponentWriter(final int arraylength) {
			this.arraylength = arraylength;
		}

		@Override
		protected double[] getComponentSlab(final Object pos) {
			return (double[]) pos;
		}

		@Override
		protected int[] makedatadimfordim(final int[] dim) {
			return ArrayUtils.add(super.makedatadimfordim(dim), arraylength);
		}

		@Override
		protected int[] putslabdimfordim(final int[] dim) {
			return ArrayUtils.add(super.putslabdimfordim(dim), 0);
		}

		@Override
		protected int[] nulldimfordim(final int[] dim) {
			return ArrayUtils.add(super.nulldimfordim(dim), 0);
		}

		@Override
		protected int[] slabsizedimfordim(final int[] dim) {
			return ArrayUtils.add(super.slabsizedimfordim(dim), arraylength);
		}
	}

	protected class PolarisationComponentWriter extends StringComponentWriter {
		ComponentWriter stokesWriter = new DoubleArrayComponentWriter(4);

		double[] getStokes(final String pos) {
			if (I05Apple.HORIZONTAL.equals(pos)) {
				return new double[] { 1.0, 1.0, 0.0, 0.0 };
			} else if (I05Apple.VERTICAL.equals(pos)) {
				return new double[] { 1.0, -1.0, 0.0, 0.0 };
			} else if (I05Apple.CIRCULAR_RIGHT.equals(pos)) {
				return new double[] { 1.0, 0.0, 0.0, 1.0 };
			} else if (I05Apple.CIRCULAR_LEFT.equals(pos)) {
				return new double[] { 1.0, 0.0, 0.0, -1.0 };
			}
			return null;
		}

		@Override
		protected byte[] getComponentSlab(final Object pos) {
			if (I05Apple.HORIZONTAL.equals(pos)) {
				return super.getComponentSlab("linear horiziontal");
			} else if (I05Apple.VERTICAL.equals(pos)) {
				return super.getComponentSlab("linear vertical");
			} else if (I05Apple.CIRCULAR_LEFT.equals(pos)) {
				return super.getComponentSlab("left circular");
			} else if (I05Apple.CIRCULAR_RIGHT.equals(pos)) {
				return super.getComponentSlab("right circular");
			}
			return super.getComponentSlab(pos);
		}

		@Override
		public Collection<SelfCreatingLink> makeComponent(final NeXusFileInterface file, final int[] dim,
				final String path, final String scannableName, final String componentName, final Object pos,
				final String unit) throws NexusException {

			super.makeComponent(file, dim, path, scannableName, componentName, pos, unit);
			final double[] stokes = getStokes(pos.toString());
			if (stokes == null) {
				stokesWriter = null;
			} else {
				stokesWriter.makeComponent(file, dim, stokesPath, scannableName, componentName, stokes, null);
			}
			return Collections.emptySet();
		}

		@Override
		public void writeComponent(final NeXusFileInterface file, final int[] start, final String path,
				final String scannableName, final String componentName, final Object pos) throws NexusException {
			super.writeComponent(file, start, path, scannableName, componentName, pos);
			final double[] stokes = getStokes(pos.toString());
			if (stokes == null) {
				stokesWriter = null;
			} else {
				stokesWriter.writeComponent(file, start, stokesPath, scannableName, componentName, stokes);
			}
		}
	}

	@Override
	protected void resetComponentWriters() {
		super.resetComponentWriters();
		getCwriter().put("polarisation", new PolarisationComponentWriter());
	}
}