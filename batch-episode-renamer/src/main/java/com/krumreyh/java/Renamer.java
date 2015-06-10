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
	 * Constructor
	 */
	public Renamer() {
	}
	
	/**
	 * Checks if a show's name is valid. All invalid characters are removed in the process.
	 * @param showName - the showname to be checked
	 * @throws IllegalArgumentException - if the name only consists of illegal characters
	 */
	public void validateShowName(String showName) throws IllegalArgumentException {
		for (int i = 0; i < this.illegalCharacters.length; i++) {
			if (showName.indexOf(this.illegalCharacters[i]) != -1) {
				 showName = showName.replace("" + this.illegalCharacters[i], "");
			}
		}
		if (showName.length() == 0) {
			throw new IllegalArgumentException();
		}
	}
	
	/**
	 * Checks if the input amount of episodes and the directory's data match up.
	 * @param firstEpString - the first episode's number as string
	 * @param lastEpString - the last episode's number as string
	 * @param directory - the directory to be used
	 * @throws IllegalArgumentException - in case the data does not match up
	 */
	public void validateEpisodeNumbers(String firstEpString,String lastEpString, String directory) throws IllegalArgumentException {
		int firstEp = Integer.parseInt(firstEpString);
		int lastEp = Integer.parseInt(lastEpString);
		int amountOfFiles = new File(directory).listFiles().length;
		if (firstEp > lastEp) {
			throw new IllegalArgumentException();
		}
		if ((lastEp - firstEp + 1) != amountOfFiles) {
			throw new IllegalArgumentException();
		}
	}
	
	/**
	 * Checks if the season number can successfully be converted to an int.
	 * Otherwise, a NumberFormatException is thrown by the Integer class.
	 * @param seasonString - the season string to be checked.
	 */
	public void validateSeasonNumber(String seasonString) {
		Integer.parseInt(seasonString);
	}
	
}
