/*
Copyright 2015-2017 Hermann Krumrey <hermann@krumreyh.com>

This file is part of folder-icon-changer.

folder-icon-changer is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

folder-icon-changer is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with folder-icon-changer.  If not, see <http://www.gnu.org/licenses/>.
*/

package com.krumreyh.java.folder.icon.changer;

import java.io.File;
import java.io.InputStream;

import com.krumreyh.java.folder.icon.changer.userinterface.gui.MainGUI;
import com.krumreyh.java.krumreylib.fileops.FileHandler;

/**
 * Class that contains the main method of the program
 * @author Hermann Krumrey
 * @version 1.0
 */
public class Main {

	/**
	 * Main method that starts the program
	 * @param args - command line parameters
	 */
	public static void main(String[] args) {
		
		if (args.length == 0) {
			new MainGUI();
		}
	}
}
