package com.krumreyh.java.batch.episode.renamer.userinterface.cli;

import java.io.IOException;

import com.krumreyh.java.batch.episode.renamer.objects.Episode;
import com.krumreyh.java.batch.episode.renamer.utils.Renamer;
import com.krumreyh.java.krumreylib.cli.CLITemplate;
import com.krumreyh.java.krumreylib.cli.TerminalParser;

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
		addCommand("", new StartRename(), CommandType.STRING, "run (Empty Input)", "Starts the renaming routine");
		addCommand("quit", new QuitCommand(), CommandType.STRING, "quit", "Terminates the program");
		addCommand("help", new HelpCommand(), CommandType.STRING, "help", "Lists all possible commands");
		start(null);
	}
	
	/**
	 * Command that starts the main renaming function
	 * @author Hermann Krumrey
	 *
	 */
	private class StartRename implements CLICommand {
		
		private String showName = "";
		private String season = "";
		private String firstEp = "";
		private String lastEp = "";
		private String directory = "";
		
		/**
		 * Starts the renaming algorithm
		 */
		public void execute() {
			boolean validInput = false;
			Renamer renamer = null;
			while (!validInput) {
				try {
					userPrompt();
					renamer = new Renamer(showName, season, firstEp, lastEp, directory);
					validInput = true;
				} catch (IllegalArgumentException e) {
					System.out.println(e.getMessage());
				}
			}
			
			Episode[] episodes = renamer.getEpisodes();
			
			for (int i = 0; i < episodes.length; i++) {
				episodes[i].setNewName(TerminalParser.prompt("Please enter the new name for: " + episodes[i].getCurrentName()));
			}
			
			renamer.setEpisodes(episodes);
			boolean confirm = false;
			episodes = renamer.getEpisodes();
			
			System.out.println("Confirm Changes:\n");
			for (int i = 0; i < episodes.length; i++) {
				System.out.println("OLD: " + episodes[i].getCurrentName());
				System.out.println("NEW: " + episodes[i].generateNewName() + "\n");
			}
			if (TerminalParser.prompt("Confirm Rename?").toLowerCase().equals("y")) {
				confirm = true;
			}
			
			if (confirm) { renamer.startRename(); }
			else { System.out.println("Operation cancelled"); }
		}
		
		/**
		 * help-method to get user input
		 */
		private void userPrompt() {
			this.showName = TerminalParser.prompt("Please enter the show name:");
			this.season = TerminalParser.prompt("Please enter the season number:");
			this.firstEp = TerminalParser.prompt("Please enter the first episode number:");
			this.lastEp = TerminalParser.prompt("Please enter the last episode number:");
			this.directory = TerminalParser.prompt("Please enter the directory to be used:");
		}
	}
}