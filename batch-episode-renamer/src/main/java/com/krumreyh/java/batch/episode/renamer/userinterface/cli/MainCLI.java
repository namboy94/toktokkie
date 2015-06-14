package com.krumreyh.java.batch.episode.renamer.userinterface.cli;

import java.io.IOException;

import com.krumreyh.java.krumreylib.cli.CLITemplate;

/**
 * Class that handles CLI In/Out-put by the user
 * @author Hermann Krumrey
 * @version 1.0
 */
public class MainCLI extends CLITemplate{

	/**
	 * Constructor that adds all possible commands to the CLI
	 */
	public MainCLI() {
		System.out.println("Batch Episode Renamer\nPress Enter to start");
		addCommand("quit", new Quit(), CommandType.STRING, "quit", "Terminates the program");
		addCommand("", new StartRename(), CommandType.STRING, "run (Empty Input)", "Starts the renaming routine");
		start();
	}
	
	/**
	 * Command that Quits the program
	 * @author Hermann Krumrey
	 */
	private class Quit implements CLICommand {
		public void execute() {
			MainCLI.this.running = false;
		}
	}
	
	/**
	 * Command that starts the main renaming function
	 * @author Hermann Krumrey
	 *
	 */
	private class StartRename implements CLICommand {
		public void execute() {
			//TODO
		}
	}
}