/*
Copyright 2015-2017 Hermann Krumrey <hermann@krumreyh.com>

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

package com.krumreyh.java.batch.episode.renamer.utils;

import java.io.File;

import com.krumreyh.java.batch.episode.renamer.objects.Episode;
import com.krumreyh.java.krumreylib.fileops.FileHandler;

/**
 * Class that handles the actual renaming of episodes
 * It gets fed by the user's frame parameters, creates Episode objects of these, returns these
 * to the User Interface for renaming and then renames the actual files accordingly
 * @author Hermann Krumrey
 * @version 1.0
 */
public class Renamer {

	private String showName;
	private int season;
	private int firstEpisode;
	private int lastEpisode;
	private File[] directoryContent;
	private Episode[] episodes;
	
	/**
	 * Constructor that gets the frame parameters of the renaming process, checks them for validity,
	 * and saves these as local variables
	 * @param showName - the show's name
	 * @param season - the show's season
	 * @param firstEp - the first episode to be renamed
	 * @param lastEp - the last episode to be renamed
	 * @param directory - the directory to be used
	 * @throws IllegalArgumentException - if an invalid parameter is entered.
	 */
	public Renamer(String showName, String season, String firstEp, String lastEp, String directory)
																	throws IllegalArgumentException {
		if (!FileHandler.checkIfDirectory(directory)) {
			throw new IllegalArgumentException("Not a Directory");
		} else {
			this.directoryContent = FileHandler.getDirectoryContent(directory);
		}
		
		this.showName = FileHandler.sanitizeFileName(showName);
		turnToInt(firstEp, lastEp, season);
		createEpisodeArray();
	}
	
	/**
	 * returns the current array of episodes for editing by a user interface
	 * @return the array of Episode objects
	 */
	public Episode[] getEpisodes() {
		return this.episodes;
	}
	
	/**
	 * Sets the new file names for the episodes after sanitizing them.
	 * @param episodes - the array of episodes containing the new episode names
	 */
	public void setEpisodes(Episode[] episodes) {
		for (int i = 0; i < episodes.length; i++) {
			this.episodes[i].setNewName(FileHandler.sanitizeFileName(episodes[i].getNewName()));
		}
	}
	
	/**
	 * Starts the rename
	 */
	public void startRename() {
		for (int i = 0; i < this.episodes.length; i++) {
			this.episodes[i].startRename();
		}
	}
	
	/**
	 * Turns the Strings the episode and season values into integer values, and saves them to private variables
	 * Also checks if this input conflicts with the given directory
	 * @param firstEp - the first episode number as string
	 * @param lastEp - the last episode number as string
	 * @param season - the season number as string
	 * @throws IllegalArgumentException - if one of the strings could not be parsed to int.
	 */
	private void turnToInt(String firstEp, String lastEp, String season) throws IllegalArgumentException {
		try {
			this.firstEpisode = Integer.parseInt(firstEp);
			this.lastEpisode = Integer.parseInt(lastEp);
			this.season = Integer.parseInt(season);
		} catch (NumberFormatException e) {
			throw new IllegalArgumentException("Not an Integer");
		}
		if (this.directoryContent.length != (this.lastEpisode - this.firstEpisode + 1)) {
			throw new IllegalArgumentException("Amount of files in directory conflicts with user input");
		}
	}
	
	/**
	 * Creates a private array of Episode objects based of the directory content previously established
	 */
	private void createEpisodeArray() {
		this.episodes = new Episode[this.directoryContent.length];
		int episodeNumber = this.firstEpisode;
		for (int i = 0; i < this.episodes.length; i++) {
			this.episodes[i] = new Episode(this.directoryContent[i], this.showName, this.season, episodeNumber);
			episodeNumber++;
		}
	}
	
}
