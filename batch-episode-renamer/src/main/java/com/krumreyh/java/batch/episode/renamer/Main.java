package com.krumreyh.java.batch.episode.renamer;

import com.krumreyh.java.batch.episode.renamer.userinterface.cli.MainCLI;
import com.krumreyh.java.batch.episode.renamer.userinterface.gui.MainGUI;

/**
 * main class that runs the program
 * @author Hermann Krumrey
 * @version 1.0
 */
public class Main {
	
	public static void main(String[] args) {
		if (args.length == 0) {
			new MainGUI();
		} else if (args[0].equals("-cli")) {
			new MainCLI();
		}
	}
	
}
