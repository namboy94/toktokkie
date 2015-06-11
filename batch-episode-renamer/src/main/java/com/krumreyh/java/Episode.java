package com.krumreyh.java;

import java.io.File;

/**
 * Class that models an episode
 * @author Hermann
 * @version 0.1
 */
public class Episode {
	
	private File episodeFile;
	private int episodeNumber;
	private int season;
	private String name;
	private String fullDirectoryPath;
	
	/**
	 * Constructor
	 * @param episodeFile - the file containing this episode
	 */
	public Episode(File episodeFile, int episodeNumber, int season) {
		this.episodeFile = episodeFile;
		this.episodeNumber = episodeNumber;
		this.season = season;
		this.name = episodeFile.getName();
		this.fullDirectoryPath = episodeFile.getAbsolutePath();
	}
	
	/**
	 * Getter-method for the episode name
	 * @return the name of the episode
	 */
	public String getName() {
		return this.name;
	}

}
