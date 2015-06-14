package com.krumreyh.java.batch.epsisode.renamer.utils;

import java.io.File;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import com.krumreyh.java.batch.episode.renamer.utils.Renamer;
import com.krumreyh.java.krumreylib.fileops.FileHandler;

/**
 * Junit Class that test the Renamer class
 * @author Hermann Krumrey
 * @version 1.0
 */
public class RenamerTest {

	private Renamer renamer;
	
	/**
	 * Sets up Junit tests
	 * Creates a new renamer object 
	 * @throws Exception - general Exception
	 */
	@Before
	public void setUp() throws Exception {
		renamer = new Renamer("Test", "1", "1", "3", "src/test/resources");
	}
	
	/**
	 * Runs at the end of every Junit test
	 * Renames all files in the resources folder back to their default names
	 * @throws Exception - general Exception
	 */
	@After
	public void tearDown() throws Exception {
		File[] files = FileHandler.getDirectoryContent("src/test/resources");
		FileHandler.renameFile(files[0], "test1");
		FileHandler.renameFile(files[1], "test2");
		FileHandler.renameFile(files[2], "test3");
	}
	
	/**
	 * Checks if the renaming works correctly
	 */
	@Test
	public void renameTest() {
		
	}
}
