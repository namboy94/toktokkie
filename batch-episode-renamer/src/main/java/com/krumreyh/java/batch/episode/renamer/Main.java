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

package com.krumreyh.java.batch.episode.renamer;

import com.krumreyh.java.batch.episode.renamer.userinterface.cli.MainCLI;
import com.krumreyh.java.batch.episode.renamer.userinterface.gui.MainGUI;

/**
 * main class that runs the program
 * @author Hermann Krumrey
 * @version 1.0
 */
public class Main {
	
	/**
	 * Main method that starts the program, has options for CLI and GUI
	 * @param args - command line parameters, -cli for CLI
	 */
	public static void main(String[] args) {
		if (args.length == 0) {
			new MainGUI();
		} else if (args[0].equals("-cli")) {
			new MainCLI();
		}
	}	
}