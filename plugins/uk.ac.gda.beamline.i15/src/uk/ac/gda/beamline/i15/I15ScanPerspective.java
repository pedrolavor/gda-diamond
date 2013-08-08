/*-
 * Copyright © 2011 Diamond Light Source Ltd.
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

package uk.ac.gda.beamline.i15;

import org.eclipse.ui.IFolderLayout;
import org.eclipse.ui.IPageLayout;
import org.eclipse.ui.IPerspectiveFactory;

public class I15ScanPerspective implements IPerspectiveFactory {
	static final String ID = "uk.ac.gda.beamline.I15ScanPerspective";

	@Override
	public void createInitialLayout(IPageLayout layout) {
		defineLayout(layout);
	}

	private void defineLayout(IPageLayout layout) {
		String editorArea = layout.getEditorArea();

		IFolderLayout leftfolder = layout.createFolder("left",
				IPageLayout.LEFT, 0.25f, editorArea);
		leftfolder.addView("gda.rcp.jythonterminalview");

		IFolderLayout bottomfolder = layout.createFolder(
				"bottom", IPageLayout.BOTTOM, 0.8f, editorArea);
		bottomfolder.addView("ch.qos.logback.eclipse.views.LogbackView");
		bottomfolder.addView("gda.rcp.datavectorview");
		bottomfolder.addView("gda.rcp.views.baton.BatonView");

		IFolderLayout middlefolder = layout.createFolder("middle",
				IPageLayout.RIGHT, 0.75f, editorArea);
		middlefolder.addView("uk.ac.gda.client.xyplotview");
		middlefolder.addView("uk.ac.diamond.scisoft.analysis.rcp.plotView1");

		IFolderLayout rightfolder = layout.createFolder("right",
				IPageLayout.RIGHT, 0.75f, "middle");
		rightfolder.addView("uk.ac.gda.exafs.ui.dashboardView");
		rightfolder.addView("uk.ac.diamond.scisoft.analysis.rcp.views.SidePlotView:Plot 1");
		rightfolder.addPlaceholder("uk.ac.diamond.scisoft.analysis.rcp.views.HistogramView:Plot 1");
		
		layout.setEditorAreaVisible(false);
	}
}