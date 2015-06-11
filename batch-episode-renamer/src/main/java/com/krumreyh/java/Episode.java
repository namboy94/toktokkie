package com.krumreyh.java;

import java.io.File;

/**
 * Class that models an episode
 * @author Hermann
 * @version 1.0
 */
public class Episode {
	
	private File episodeFile;
	private int episodeNumber;
	private int season;
	private String showName;
	private String name;
	private String fullDirectoryPath;
	private String fileExtension;
	
	/**
	 * Constructor
	 * @param episodeFile - the file containing this episode
	 */
	public Episode(File episodeFile, int episodeNumber, int season, String showName) {
		this.episodeFile = episodeFile;
		this.episodeNumber = episodeNumber;
		this.season = season;
		this.showName = showName;
		this.name = episodeFile.getName();
		this.fullDirectoryPath = episodeFile.getAbsolutePath();
		this.fileExtension = getFileExtension(this.episodeFile);
	}
	
	/**
	 * Getter-method for the episode name
	 * @return the name of the episode
	 */
	public String getName() {
		return this.name;
	}
	
	/**
	 * Getter-method for the show name
	 * @return the name of the show
	 */
	public String getShowName() {
		return this.showName;
	}
	
	/**
	 * Getter-method for the file's extension
	 * @return the file extension of the episode file
	 */
	public String getFileExtension() {
		return this.fileExtension;
	}
	
	/**
	 * Getter-method that return the file in which the episode is saved
	 * @return the episode's file
	 */
	public File getFile() {
		return this.episodeFile;
	}
	
	/**
	 * Returns the episode number as string, at least two digits long
	 * @return the episode number
	 */
	public String getEpisode() {
		return turnIntToString(this.episodeNumber);
	}
	
	/**
	 * Returns the season number as string, at least two digits long
	 * @return the season number
	 */
	public String getSeason() {
		return turnIntToString(this.season);
	}
	
	/**
	 * Turns an int into a string and appends a '0' to the beginning if th int is < 10
	 * @return the int as string
	 */
	private String turnIntToString(int input) {
		String output = "";
		if (input < 10) {
			output = "0" + input;
		} else {
			output = "" + input;
		}
		return output;
	}
	
	/**
	 * Analyzes a file for its file extension and returns it as String 
	 * @param file - the file to be analyzed
	 * @return the file extension as String
	 */
	private String getFileExtension(File file) {
		String fileName = file.getName();
		String fileExtension = fileName.substring(fileName.lastIndexOf(".") + 1);
		return fileExtension;
	}
}
