package com.krumreyh.java;

import com.krumreyh.java.user.interfaces.MainCLI;

/**
 * Main Class of the batch episode renamer
 * @author Hermann Krumrey
 * @version 1.0
 */
public class Main {

	/**
	 * main method that starts the user interface and renames the episodes according to the
	 * HK-plex-conform episode file format
	 * @param args - command line parameter
	 */
	public static void main(String[] args) {
		
		if (args.length == 0) {
			new MainGUI();
		} else if (args[0].equals("-cli")) {
			new MainCLI();
		}
	}
}
