package com.krumreyh.java;

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
		} else {
			System.out.println("Too many arguments");
		}
	}
}
