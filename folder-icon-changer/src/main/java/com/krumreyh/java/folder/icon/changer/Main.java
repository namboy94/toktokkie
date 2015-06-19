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
