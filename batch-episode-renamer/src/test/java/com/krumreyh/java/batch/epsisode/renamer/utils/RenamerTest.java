package com.krumreyh.java.batch.epsisode.renamer.utils;

import static org.junit.Assert.fail;

import java.io.File;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import com.krumreyh.java.batch.episode.renamer.objects.Episode;
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
		renamer = new Renamer("Test", "1", "1", "3", "src/test/resources/testDir");
	}
	
	/**
	 * Runs at the end of every Junit test
	 * Renames all files in the resources folder back to their default names
	 * @throws Exception - general Exception
	 */
	@After
	public void tearDown() throws Exception {
		File[] files = FileHandler.getDirectoryContent("src/test/resources/testDir");
		FileHandler.renameFile(files[0], "test1");
		FileHandler.renameFile(files[1], "test2");
		FileHandler.renameFile(files[2], "test3");
	}
	
	/**
	 * Checks if the renaming works correctly
	 */
	@Test
	public void renameTest() {
		Episode[] episodes = renamer.getEpisodes();
		episodes[0].setNewName("TestRename1");
		episodes[1].setNewName("TestRename2");
		episodes[2].setNewName("TestRename3");
		renamer.setEpisodes(episodes);
		renamer.startRename();
		
		if (!FileHandler.checkifFile("src/test/resources/testDir/Test - S01E01 - TestRename1.txt")) { fail(); }
		if (!FileHandler.checkifFile("src/test/resources/testDir/Test - S01E02 - TestRename2.txt")) { fail(); }
		if (!FileHandler.checkifFile("src/test/resources/testDir/Test - S01E03 - TestRename3.txt")) { fail(); }
	}
}
