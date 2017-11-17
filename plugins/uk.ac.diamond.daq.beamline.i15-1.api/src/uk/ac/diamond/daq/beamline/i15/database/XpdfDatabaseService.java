/*-
 * Copyright © 2017 Diamond Light Source Ltd.
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

package uk.ac.diamond.daq.beamline.i15.database;

import java.sql.SQLException;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

import org.osgi.service.component.annotations.Activate;
import org.osgi.service.component.annotations.Component;
import org.osgi.service.component.annotations.Reference;
import org.osgi.service.component.annotations.ReferenceCardinality;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import gda.configuration.properties.LocalProperties;
import uk.ac.diamond.ispyb.api.DataCollectionPlan;
import uk.ac.diamond.ispyb.api.IspybXpdfApi;
import uk.ac.diamond.ispyb.api.IspybXpdfFactoryService;
import uk.ac.diamond.ispyb.api.Sample;
import uk.ac.diamond.ispyb.api.Schema;


/**
 * Class to provide XPDF access to the ISPyB database as a OSGi service.
 * <p>
 * Implementation details:
 * <li>It needs to be lazy started as it need to use properties for the DB connection parameters. During the startup of
 * OSGi these properties will not be correctly accessed see
 * <a href="http://jira.diamond.ac.uk/browse/DAQ-836">DAQ-836</a>
 * <li>It is using the OSGi annotations with the Eclipse DS annotation builder to auto-generate the component.xml files
 *
 * @author James Mudd
 */
@Component(name="XpdfDatabaseService", immediate=false)
public class XpdfDatabaseService implements IXpdfDatabaseService {
	private static final Logger logger = LoggerFactory.getLogger(XpdfDatabaseService.class);

	private static final String XPDF_URL_PROP = "xpdf.server.ispyb.connector.url";
	private static final String XPDF_USER_PROP = "xpdf.server.ispyb.connector.user";
	private static final String XPDF_PASSWORD_PROP = "xpdf.server.ispyb.connector.password";
	private static final String XPDF_DATABASE_PROP = "xpdf.server.ispyb.connector.database";

	private IspybXpdfFactoryService factoryService;
	private IspybXpdfApi api;

	@Activate
	public void activate() {
		logger.debug("Activating...");
		final String url = getUrl();
		final Optional<String> username = getUsername();
		final Optional<String> password = getPassword();
		final Optional<String> database = getDatabase();

		try {
			api = factoryService.buildIspybApi(url, username, password, database);
		} catch (SQLException e) {
			logger.error("Failed to connect to ISPyB", e);
			throw new RuntimeException("Failed to connect to ISPyB", e);
		}
		logger.info("Sucessfully connected to ISPyB");
	}

	@Override
	public Map<Long, String> getSampleIdNames(String proposalCode, long proposalNumber) {
		List<Sample> samples = getSamples(proposalCode, proposalNumber);

		// Transform to the required map
		return samples.stream().collect(Collectors.toMap(Sample::getSampleId, Sample::getSampleName));
	}

	@Override
	public List<Sample> getSamples(String proposalCode, long proposalNumber) {
		if (proposalCode.length() > 3) {
			throw new IllegalArgumentException("proposalCode mush be <=3 characters eg 'cm'");
		}

		// Access the DB
		return  api.retrieveSamplesAssignedForProposal(proposalCode, proposalNumber);
	}

	@Override
	public Sample getSampleInformation(String proposalCode, long proposalNumber, long sampleId) {
		return getSamples(proposalCode, proposalNumber).stream(). // Get all samples for proposal
				filter(s -> s.getSampleId().longValue() == sampleId). // find the one with right ID
				findFirst(). // Get as a Optional<Samples>
				orElseThrow(() -> new IllegalArgumentException("No sample exisits with that ID")); // Throw if it doesn't exist else return
	}

	@Override
	public List<DataCollectionPlan> getDataCollectionPlanForSample(long sampleId) {
		return api.retrieveDataCollectionPlansForSample(sampleId);
	}

	private String getUrl() {
		final String url = LocalProperties.get(XPDF_URL_PROP);
		if(url == null) {
			final String msg = "No DB URL defined by property: " + XPDF_URL_PROP;
			logger.error(msg); // Log here additionally as exception is caught by OSGi framework.
			throw new IllegalStateException(msg);
		}
		return LocalProperties.get(XPDF_URL_PROP);
	}

	/**
	 * The MariaDB hosting IspyB host several other databases see <a href="http://confluence.diamond.ac.uk/display/SCI/Database+Systems">Database Systems</a>
	 *
	 * @return Database name
	 */
	private Optional<String> getDatabase() {
		final String database = LocalProperties.get(XPDF_DATABASE_PROP);
		if (database == null || database.isEmpty()) {
			final String msg = "No database defined by property: " + XPDF_DATABASE_PROP;
			logger.error(msg); // Log here additionally as exception is caught by OSGi framework.
			throw new IllegalStateException(msg);
		}
		return Optional.of(Schema.convert(database).toString());
	}

	private Optional<String> getPassword() {
		// If the password contains commas it will be split into a list which is not what is wanted here so join it again.
		final String password = String.join(",", LocalProperties.getStringArray(XPDF_PASSWORD_PROP));
		if (password == null || password.isEmpty()) {
			final String msg = "No DB password defined by property: " + XPDF_PASSWORD_PROP;
			logger.error(msg); // Log here additionally as exception is caught by OSGi framework.
			throw new IllegalStateException(msg);
		}
		return Optional.of(password);
	}

	private Optional<String> getUsername() {
		final String username = LocalProperties.get(XPDF_USER_PROP);
		if (username == null || username.isEmpty()) {
			final String msg = "No DB username defined by property: " + XPDF_USER_PROP;
			logger.error(msg); // Log here additionally as exception is caught by OSGi framework.
			throw new IllegalStateException(msg);
		}
		return Optional.of(LocalProperties.get(XPDF_USER_PROP));
	}

	@Reference(cardinality=ReferenceCardinality.MANDATORY)
	public synchronized void setFactoryService(IspybXpdfFactoryService factoryService) {
		this.factoryService = factoryService;
		logger.debug("Set IspybXpdfFactoryService to {}", factoryService);
	}

}