package com.krumreyh.java.user.interfaces;

import java.io.IOException;

import com.krumreyh.java.krumreylib.cli.CLITemplate;

/**
 * Class that handles CLI In/Out-put by the user
 * @author Hermann Krumrey
 * @version 1.0
 */
public class MainCLI extends CLITemplate{

	public MainCLI() {
		addCommand("quit", new Quit(), CommandType.STRING);
		try { start(); } catch (IOException e) {}
	}
	
	private class Quit implements CLICommand {
		public void execute() {
			MainCLI.this.running = false;
		}
	}
}
