package com.krumreyh.java.batch.episode.renamer.userinterface.gui;

import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JTextField;

import com.krumreyh.java.batch.episode.renamer.objects.Episode;
import com.krumreyh.java.batch.episode.renamer.utils.Renamer;
import com.krumreyh.java.krumreylib.gui.swing.GUITemplate;

/**
 * Class that models the primary GUI of the application
 * @author Hermann Krumrey
 * @version 1.0
 */
public class MainGUI extends GUITemplate {

	protected JTextField showNameField;
	protected JTextField seasonField;
	protected JTextField firstEpField;
	protected JTextField lastEpField;
	protected JTextField directoryField;
	
	
	/**
	 * Constructor that adds all GUI Elements and starts the GUI
	 */
	public MainGUI() {
		
		setGUISettings("Batch Episode Renamer", 250, 250, 400, 470, null, EXIT_ON_CLOSE, false);
		
		//Add UI Elements
		addLabel("Show Name", 10, 10, 100, 50);
		addLabel("Season", 10, 70, 100, 50);
		addLabel("First Episode", 10, 130, 100, 50);
		addLabel("Last Episode", 10, 190, 100, 50);
		addLabel("Directory", 10, 250, 100, 50);
		this.showNameField = addTextField("", 120, 10, 270, 50);
		this.seasonField = addTextField("", 120, 70, 270, 50);
		this.firstEpField = addTextField("", 120, 130, 270, 50);
		this.lastEpField = addTextField("", 120, 190, 270, 50);
		this.directoryField = addTextField("", 120, 250, 270, 50);
		changeComponentAppearance(addButton("Start Renaming", 25, 350, 350, 60, new StartButton()), 20, 0, "arial",
																		new Color(255, 255, 255), new Color(0, 0, 0));
		
		startGUI();
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
				JOptionPane.showMessageDialog(MainGUI.this, e.getMessage());
				return;
			}
			
			Episode[] episodes = renamer.getEpisodes();
			
			for (int i = 0; i < episodes.length; i++) {
				JFrame frame = new JFrame("New Episode Name");
				String prompt = JOptionPane.showInputDialog(frame, "Enter the new episode name for: \n"
																		+ episodes[i].getCurrentName());
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
				JOptionPane.showMessageDialog(MainGUI.this, "Operation aborted");
			} else {
				renamer.startRename();
			}	
		}
		
		/**
		 * Prompts the user for confirmation of an episode rename
		 */
		private boolean confirmationPrompt(Episode episode) {
			int confirmed = JOptionPane.YES_NO_OPTION;
			String message = "Rename\n\n" + episode.getCurrentName() + "\n\nto:\n\n"
												+ episode.generateNewName() + "\n\n?";
			confirmed = JOptionPane.showConfirmDialog(MainGUI.this, message, "Rename Confirmation", confirmed);
			return (confirmed == 0);
		}
	}
}
