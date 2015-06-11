package com.krumreyh.java;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;

/**
 * Class that bundles all relevant methods to rename episodes
 * @author Hermann Krumrey
 * @version 1.0
 */
public class Renamer {

	private char[] illegalCharacters =  {'<', '>', ':', '\"', '/', '\\', '|', '?', '*'};
	private String showName;
	private int season;
	private int firstEp;
	private int lastEp;
	private String directory;
	private File[] directoryContent;
	private Episode[] episodes;
	private String[] newEpisodeNames;
	
	/**
	 * Constructor of the Renamer class that automagically tests the input parameters for validity
	 * @param showName - the show's name
	 * @param season - the season number
	 * @param firstEp - the first episode's number
	 * @param lastEp - the last episode's number
	 * @param directory - the directory to be used
	 * @throws IllegalArgumentException - if an illegal argument is found
	 */
	public Renamer(String showName, String season, String firstEp, String lastEp, String directory) throws IllegalArgumentException{
		validateShowName(showName);
		validateIntegerConversion(season);
		validateEpisodeNumbers(firstEp, lastEp, directory);
		
		this.showName = showName;
		this.season = Integer.parseInt(season);
		this.firstEp = Integer.parseInt(firstEp);
		this.lastEp = Integer.parseInt(lastEp);
		this.directory = directory;
		
		this.directoryContent = getAndSortDirectoryContent();
		this.episodes = createEpisodes(this.directoryContent);
	}
	
	/**
	 * Getter-Method for the array of episodes
	 * @return the array of episodes
	 */
	public Episode[] getEpisodes() {
		return this.episodes;
	}
	
	/**
	 * Sets the new episode names
	 * @param newEpisodeNames - array of new episode names
	 */
	public void setNewEpisodeNames(String[] newEpisodeNames) {
		this.newEpisodeNames = newEpisodeNames;
	}
	
	/**
	 * Renames all episodes in the episodes Array with the names from the array newEpisodeNames
	 * @throws IOException - if the system command fails
	 */
	public void startRename() {
		for (int i = 0; i < this.episodes.length; i++) {
			String newFile = this.directory + this.showName + " - S" + this.episodes[i].getSeason();
			newFile += "E" + this.episodes[i].getEpisode() + " - " + this.newEpisodeNames[i] + "." + this.episodes[i].getFileExtension();
			this.episodes[i].getFile().renameTo(new File(newFile));
		}
	}
	
	/**
	 * Checks if a show's name is valid. All invalid characters are removed in the process.
	 * @param showName - the showname to be checked
	 * @throws IllegalArgumentException - if the name only consists of illegal characters
	 */
	private void validateShowName(String showName) throws IllegalArgumentException {
		String illegalNameError = "The show name consists of no valid characters";
		
		for (int i = 0; i < this.illegalCharacters.length; i++) {
			if (showName.indexOf(this.illegalCharacters[i]) != -1) {
				 showName = showName.replace("" + this.illegalCharacters[i], "");
			}
		}
		if (showName.length() == 0) {
			throw new IllegalArgumentException(illegalNameError);
		}
	}
	
	/**
	 * Checks if the input amount of episodes and the directory's data match up.
	 * @param firstEpString - the first episode's number as string
	 * @param lastEpString - the last episode's number as string
	 * @param directory - the directory to be used
	 * @throws IllegalArgumentException - in case the data does not match up
	 * @throws NumberFormatException - in case the episode strings are not convertable to int
	 */
	private void validateEpisodeNumbers(String firstEpString,String lastEpString, String directory)
	throws IllegalArgumentException {
		validateIntegerConversion(firstEpString);
		validateIntegerConversion(lastEpString);
		validateDirectory(directory);
		String largerFirstEpError = "The first Episode is higher than the last episode";
		String amountOfEpsError = "The given amount of episodes do not coincide with the amount of " +
								  "files in the specified directory";
		int firstEp = Integer.parseInt(firstEpString);
		int lastEp = Integer.parseInt(lastEpString);
		int amountOfFiles = new File(directory).listFiles().length;
		if (firstEp > lastEp) { throw new IllegalArgumentException(largerFirstEpError); }
		if ((lastEp - firstEp + 1) != amountOfFiles) { throw new IllegalArgumentException(amountOfEpsError); }
	}
	
	/**
	 * Checks if a string can be converted to an int, else an IllegalArgumentException
	 * is thrown.
	 * @param intAsString - the string to be checked.
	 * @throws NumberFormatException - if the string isn't converted correctly
	 */
	private void validateIntegerConversion(String intAsString) throws IllegalArgumentException {
		try {
			Integer.parseInt(intAsString);
		} catch (NumberFormatException e) {
			String errorMessage = "\"" + intAsString + "\" is not a valid integer value";
			throw new IllegalArgumentException(errorMessage);
		}
	}
	
	/**
	 * Checks if a directory is valid
	 * @param directory - the directory to be checked
	 * @throws IllegalArgumentException - in case the directory is not valid
	 */
	private void validateDirectory(String directory) throws IllegalArgumentException{
		try {
			if (!new File(directory).exists()) { 
				throw new IllegalArgumentException("Directory not valid");
			}
			if (!directory.endsWith("/") && !directory.endsWith("\\")) {
				throw new IllegalArgumentException("Directory does not end with / or \\");
			}
		} catch (NullPointerException e) {
			throw new IllegalArgumentException("Directory not valid");
		}
	}
	
	/**
	 * Gets an array of files containing the files in the directory used.
	 * @return the files in an array of files
	 */
	private File[] getAndSortDirectoryContent() {
		File[] listOfFiles = new File(this.directory).listFiles();
		Arrays.sort(listOfFiles);
		return listOfFiles;
	}
	
	/**
	 * Creates an array of episodes based on the content of the directory
	 * @param listOfFiles - the files to be added to the episodes
	 * @return the array of Episodes
	 */
	private Episode[] createEpisodes(File[] listOfFiles) {
		Episode[] episodes = new Episode[(this.lastEp - this.firstEp + 1)];
		int currentEpisode = this.firstEp;
		for (int i = 0; i < listOfFiles.length; i++) {
			episodes[i] = new Episode(listOfFiles[i], currentEpisode, this.season, this.showName);
			currentEpisode++;
		}
		return episodes;
	}
}