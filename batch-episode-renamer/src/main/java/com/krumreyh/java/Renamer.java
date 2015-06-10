package com.krumreyh.java;

import java.io.File;

/**
 * Class that bundles all relevant methods to rename episodes
 * @author Hermann Krumrey
 * @version 0.1
 */
public class Renamer {

	char[] illegalCharacters =  {'<', '>', ':', '\"', '/', '\\', '|', '?', '*'};
	
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
		} catch (NullPointerException e) {
			throw new IllegalArgumentException("Directory not valid");
		}
	}
	
}
