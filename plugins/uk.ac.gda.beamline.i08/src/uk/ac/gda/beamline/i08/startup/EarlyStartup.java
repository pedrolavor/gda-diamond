/*-
 * Copyright © 2010 Diamond Light Source Ltd.
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

package uk.ac.gda.beamline.i08.startup;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;

import org.eclipse.core.commands.ExecutionException;
import org.eclipse.core.commands.NotEnabledException;
import org.eclipse.core.commands.NotHandledException;
import org.eclipse.core.commands.common.NotDefinedException;
import org.eclipse.swt.widgets.Display;
import org.eclipse.swt.widgets.Event;
import org.eclipse.ui.IEditorInput;
import org.eclipse.ui.IEditorPart;
import org.eclipse.ui.IEditorReference;
import org.eclipse.ui.IPartListener;
import org.eclipse.ui.IPartService;
import org.eclipse.ui.IPerspectiveDescriptor;
import org.eclipse.ui.IStartup;
import org.eclipse.ui.IViewReference;
import org.eclipse.ui.IWorkbenchPage;
import org.eclipse.ui.IWorkbenchPart;
import org.eclipse.ui.IWorkbenchWindow;
import org.eclipse.ui.PerspectiveAdapter;
import org.eclipse.ui.PlatformUI;
import org.eclipse.ui.handlers.IHandlerService;
import org.eclipse.ui.part.EditorPart;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import uk.ac.gda.client.experimentdefinition.components.ExperimentExperimentView;
import uk.ac.gda.client.experimentdefinition.components.ExperimentPerspective;
import uk.ac.gda.client.experimentdefinition.ui.handlers.RefreshProjectCommandHandler;
import uk.ac.gda.client.microfocus.ui.MicroFocusPerspective;
import uk.ac.gda.client.microfocus.views.ExafsSelectionView;

public class EarlyStartup implements IStartup {

	private static final Logger logger = LoggerFactory.getLogger(EarlyStartup.class);

	private HashMap<String, ArrayList<IEditorReference>> perspectiveEditors = new HashMap<String, ArrayList<IEditorReference>>();
	private HashMap<String, IEditorReference> lastActiveEditors = new HashMap<String, IEditorReference>();

	@Override
	public void earlyStartup() {
		Display.getDefault().asyncExec(new Runnable() {

			@Override
			public void run() {

				setupPartListener();
				final IWorkbenchWindow workbenchWindow = PlatformUI.getWorkbench().getActiveWorkbenchWindow();
				if (workbenchWindow != null) {
					workbenchWindow.addPerspectiveListener(new PerspectiveAdapter() {

						@Override
						public void perspectiveActivated(IWorkbenchPage page, IPerspectiveDescriptor perspective) {
							super.perspectiveActivated(page, perspective);
							if (perspective.getId().indexOf(MicroFocusPerspective.ID) > -1) {
								IViewReference[] viewReference = page.getViewReferences();
								for (IViewReference view : viewReference) {
									if (view.getId().equals(ExafsSelectionView.ID)) {
										((ExafsSelectionView) view.getView(true)).refresh();
									}
								}

							} else if (perspective.getId().indexOf(ExperimentPerspective.ID) > -1) {
								IViewReference[] viewReference = page.getViewReferences();
								for (IViewReference view : viewReference) {
									if (view.getId().equals(ExperimentExperimentView.ID)) {
										IHandlerService handlerService = (IHandlerService) ((ExperimentExperimentView) view
												.getView(true)).getSite().getService(IHandlerService.class);
										// Execute the command
										try {
											handlerService.executeCommand(RefreshProjectCommandHandler.ID, new Event());
										} catch (ExecutionException e) {
											logger.error("Error during refresh ", e);
										} catch (NotDefinedException e) {
											logger.error("Error during refresh ", e);
										} catch (NotEnabledException e) {
											logger.error("Error during refresh ", e);
										} catch (NotHandledException e) {
											logger.error("Error during refresh ", e);
										}
									}
								}

							}

							/*----------------------------------------------
							 * part to hide all open editors
							 */
							// Hide all the editors
							IEditorReference[] editors = page.getEditorReferences();
							for (int i = 0; i < editors.length; i++) {
								page.hideEditor(editors[i]);
							}

							// Show the editors associated with this perspective
							ArrayList<IEditorReference> editorRefs = perspectiveEditors.get(perspective.getId());
							if (editorRefs != null) {
								for (Iterator<IEditorReference> it = editorRefs.iterator(); it.hasNext();) {
									IEditorReference editorInput = it.next();
									page.showEditor(editorInput);
								}

								// Send the last active editor to the top
								IEditorReference lastActiveRef = lastActiveEditors.get(perspective.getId());
								if (lastActiveRef != null)
									page.bringToTop(lastActiveRef.getPart(true));
							}
							/*-----Part to hide all editor**/

						}

						@Override
						public void perspectiveDeactivated(IWorkbenchPage page, IPerspectiveDescriptor perspective) {
							// updateTitle();
							IEditorPart activeEditor = page.getActiveEditor();
							if (activeEditor != null) {

								// Find the editor reference that relates to this editor input
								IEditorReference[] editorRefs = page.findEditors(activeEditor.getEditorInput(), null,
										IWorkbenchPage.MATCH_INPUT);
								if (editorRefs.length > 0) {
									lastActiveEditors.put(perspective.getId(), editorRefs[0]);
								}
							}
						}

					});
				}
			}
		});
	}

	private void setupPartListener() {
		final IWorkbenchWindow workbenchWindow = PlatformUI.getWorkbench().getActiveWorkbenchWindow();
		IPartService service = (IPartService) workbenchWindow.getService(IPartService.class);
		service.addPartListener(new IPartListener() {

			@Override
			public void partActivated(IWorkbenchPart part) {
			}

			@Override
			public void partBroughtToTop(IWorkbenchPart part) {
			}

			@Override
			public void partClosed(IWorkbenchPart part) {
			}

			@Override
			public void partDeactivated(IWorkbenchPart part) {
			}

			@Override
			public void partOpened(IWorkbenchPart part) {
				if (part instanceof EditorPart) {
					EditorPart editor = (EditorPart) part;
					IWorkbenchPage page = part.getSite().getPage();
					IEditorInput editorInput = editor.getEditorInput();
					IPerspectiveDescriptor activePerspective = page.getPerspective();

					ArrayList<IEditorReference> editors = perspectiveEditors.get(activePerspective.getId());
					if (editors == null)
						editors = new ArrayList<IEditorReference>();

					// Find the editor reference that relates to this editor input
					IEditorReference[] editorRefs = page.findEditors(editorInput, null, IWorkbenchPage.MATCH_INPUT);

					if (editorRefs.length > 0) {
						editors.add(editorRefs[0]);
						perspectiveEditors.put(activePerspective.getId(), editors);
					}
				}
			}
		});

	}
}
