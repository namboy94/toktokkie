/*
Copyright 2015-2017 Hermann Krumrey

This file is part of batch-episode-renamer.

batch-episode-renamer is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

batch-episode-renamer is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with batch-episode-renamer.  If not, see <http://www.gnu.org/licenses/>.
*/

package com.krumreyh.java.batch.episode.renamer.objects;

import java.io.File;

import com.krumreyh.java.krumreylib.fileops.FileHandler;

/**
 * Class that models an episode
 * @author Hermann Krumrey
 * @version 1.0
 */
public class Episode {

	private File episodeFile;
	private String showName;
	private int seasonNumber;
	private int episodeNumber;
	private String episodeName;
	private String renameTo = "";

	/**
	 * Constructor that feeds the metadata of the episode to the object
	 * @param episodeFile - the file in which the episodes resides
	 * @param showName - the show's name to which this episode belongs to
	 * @param seasonNumber - the season to which this episode belongs to
	 * @param episodeNumber - the episode's episode number
	 */
	public Episode(File episodeFile, String showName, int seasonNumber, int episodeNumber) {
		this.episodeFile = episodeFile;
		this.showName = showName;
		this.seasonNumber = seasonNumber;
		this.episodeNumber = episodeNumber;
		this.episodeName = FileHandler.getPureFileName(episodeFile);
	}
	
	/**
	 * Sets a new name for renaming
	 * @param newName - the new name of the episode
	 */
	public void setNewName(String newName) {
		this.renameTo = newName;
	}
	
	/**
	 * getter-method that delivers the new would-be name of the episode
	 * @return the new name of the episode
	 */
	public String getNewName() {
		return this.renameTo;
	}
	
	/**
	 * Return the current name of the file the episode is contained in.
	 * @return - the current episode name
	 */
	public String getCurrentName() {
		return this.episodeName;
	}
	
	/**
	 * Generates the new File name of the episode and returns it. It is publicly visible so that it can be used
	 * in confirmation dialogues
	 * @return the new file name of the file after a potential rename
	 */
	public String generateNewName() {
		String episodeString = integerToString(this.episodeNumber);
		String seasonString = integerToString(this.seasonNumber);
		return this.showName + " - S" + seasonString + "E" + episodeString + " - " + this.renameTo;
	}
	
	/**
	 * Renames the episode to the String saved in renameTo
	 */
	public void startRename() {
		String newFileName = generateNewName();
		FileHandler.renameFile(this.episodeFile, newFileName);
		this.episodeFile = new File(this.renameTo);
		this.episodeName = this.renameTo;
		this.renameTo = "";
	}
	
	/**
	 * Converts an integer to a String to accomodate the common convention of having episode and season numbers
	 * be preceeded by a 0 when they are below 10.
	 * @param integer - the integer value to be converted
	 * @return the integer value as episode/season conform string
	 */
	private String integerToString(int integer) {
		if (integer < 10) {
			return "0" + integer;
		} else {
			return "" + integer;
		}
	}
	
}
