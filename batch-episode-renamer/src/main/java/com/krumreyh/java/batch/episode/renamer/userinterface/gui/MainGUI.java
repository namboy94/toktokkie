package com.krumreyh.java.batch.episode.renamer.userinterface.gui;

import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JTextField;

import com.krumreyh.java.batch.episode.renamer.objects.Episode;
import com.krumreyh.java.batch.episode.renamer.utils.Renamer;
import com.krumreyh.java.krumreylib.gui.swing.config.StyleConfig;
import com.krumreyh.java.krumreylib.gui.swing.config.themes.KrumreyDefault;
import com.krumreyh.java.krumreylib.gui.swing.templates.BasicGUI;

/**
 * Class that models the primary GUI of the application
 * @author Hermann Krumrey
 * @version 1.0
 */
public class MainGUI extends BasicGUI {

	protected JTextField showNameField;
	protected JTextField seasonField;
	protected JTextField firstEpField;
	protected JTextField lastEpField;
	protected JTextField directoryField;
	
	
	/**
	 * Constructor that adds all GUI Elements and starts the GUI
	 */
	public MainGUI() {
		
		this.setGUISettings("Batch Episode Renamer", 400, 420, null, EXIT_ON_CLOSE, false, new KrumreyDefault());
		
		//Add UI Elements
		addLabel("Show Name", 10, 10, 100, 50);
		addLabel("Season", 10, 70, 100, 50);
		addLabel("First Episode", 10, 130, 100, 50);
		addLabel("Last Episode", 10, 190, 100, 50);
		addLabel("Directory", 10, 250, 100, 50);
		this.showNameField = this.addTextField("", 120, 10, 270, 50, null);
		this.seasonField = this.addTextField("", 120, 70, 270, 50, null);
		this.firstEpField = addTextField("", 120, 130, 270, 50, null);
		this.lastEpField = addTextField("", 120, 190, 270, 50, null);
		this.directoryField = addTextField("", 120, 250, 270, 50, null);
		addButton("Start Renaming", 25, 330, 350, 60, new StartButton());
		
		this.setVisible(true);
	}
	
	
	/**
	 * Class that implements an ActionListener for the 'Start Renaming' button of the GUI
	 * @author Hermann Krumrey
	 */
	protected class StartButton implements ActionListener {
		/**
		 * The action performed by the button
		 * @param ae - the button-press event
		 */
		public void actionPerformed(ActionEvent ae) {
			
			String showName = MainGUI.this.showNameField.getText();
			String season = MainGUI.this.seasonField.getText();
			String firstEp = MainGUI.this.firstEpField.getText();
			String lastEp = MainGUI.this.lastEpField.getText();
			String directory = MainGUI.this.directoryField.getText();
			Renamer renamer = null;
			
			try {
				renamer = new Renamer(showName, season, firstEp, lastEp, directory);
			} catch (IllegalArgumentException e) {
				showMessageBox(e.getMessage(), "Illegal Argument Exception", -1, -1);
				return;
			}
			
			Episode[] episodes = renamer.getEpisodes();
			
			for (int i = 0; i < episodes.length; i++) {
				String message ="Enter the new episode name for: \n" + episodes[i].getCurrentName();
				String prompt = showInputDialog(message, "New Episode Name", -1, -1);
				episodes[i].setNewName(prompt);
			}
			
			renamer.setEpisodes(episodes);
			episodes = renamer.getEpisodes();
			
			boolean confirmed = true;
			for (int i = 0; i < episodes.length; i++) {
				confirmed = confirmationPrompt(episodes[i]);
				if (!confirmed) {
					break;
				}
			}
			
			if (!confirmed) {
				showMessageBox("Operation Aborted", "Operation Aborted", -1, -1);
			} else {
				renamer.startRename();
			}	
		}
		
		/**
		 * Prompts the user for confirmation of an episode rename
		 */
		private boolean confirmationPrompt(Episode episode) {
			String message = "Rename\n\n" + episode.getCurrentName() + "\n\nto:\n\n"
												+ episode.generateNewName() + "\n\n?";
			return MainGUI.this.showConfirmationPrompt(message, "Rename Confirmation", -1, -1);
		}
	}
}
