package com.krumreyh.java;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

/**
 * JUnit class that tests the Renamer class
 * @author Hermann Krumrey
 * @version 1.0
 */
public class RenamerTest {

	/**
	 * Set-up method
	 * @throws Exception - General Exception
	 */
	@Before
	public void setUp() throws Exception {
	}
	
	/**
	 * Tear-Down Method
	 * @throws Exception - General Exception
	 */
	@After
	public void tearDown() throws Exception {
	}
	
	@Test
	public void testRename() {
		Renamer testRenamer = new Renamer("test", "1", "1", "5", "src/test/resources/testDirectory/");
		String[] newNames = {"1", "\"test\"", "3", "4", "5"};
		testRenamer.setNewEpisodeNames(newNames);
		testRenamer.startRename();
	}
}
