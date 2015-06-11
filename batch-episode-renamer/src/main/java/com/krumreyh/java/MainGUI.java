package com.krumreyh.java;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JTextField;

/**
 * Class that implements a GUI using Swing
 * @author Hermann Krumrey
 * @versio 1.0
 */
public class MainGUI extends JFrame{

	protected JTextField showNameField;
	protected JTextField seasonField;
	protected JTextField firstEpField;
	protected JTextField lastEpField;
	protected JTextField directoryField;
	
	/**
	 * Constructor of the GUI that adds all UI elements
	 */
	public MainGUI() {
		
		//Set GUI parameters
		this.setTitle("Batch Episode Renamer");
		this.setLocation(250, 250);
		this.setSize(400, 470);
		this.setLayout(null);
		this.setDefaultCloseOperation(EXIT_ON_CLOSE);
		this.setResizable(false);
		
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
		addButton("Start Renaming", 25, 350, 350, 60, new StartButton());
		
		//Set GUI to visible
		this.setVisible(true);
	}
	
	/**
	 * adds a text field to the GUI with the specified parameters.
	 * @param text - the text to be displayed initially
	 * @param xPos - the x-position of the field
	 * @param yPos - the y-position of the field
	 * @param width - the width of the field
	 * @param height - the height of the field
	 * @return the JTextField object created, so that it's content can be used later on
	 */
	protected JTextField addTextField(String text, int xPos, int yPos, int width, int height) {
		JTextField textField = new JTextField(text);
		textField.setLocation(xPos, yPos);
		textField.setSize(width, height);
		this.add(textField);
		return textField;
	}
	
	/**
	 * adds a label to the GUI with the specified parameters.
	 * @param text - the text to be displayed
	 * @param xPos - the x-position of the field
	 * @param yPos - the y-position of the field
	 * @param width - the width of the field
	 * @param height - the height of the field
	 * @return the created JLabel, in case it's information is needed later on
	 */
	protected JLabel addLabel(String text, int xPos, int yPos, int width, int height) {
		JLabel label = new JLabel(text);
		label.setLocation(xPos, yPos);
		label.setSize(width, height);
		this.add(label);
		return label;
	}
	
	/**
	 * Adds a button to the GUI
	 * @param text - the text to be displayed on the button
	 * @param xPos - the x-position of the button
	 * @param yPos - the y-position of the button
	 * @param width - the width of the button
	 * @param height - the height of the button
	 * @param listener - the command to be executed when the button is pressed
	 * @return the created JButton, in case it's information is needed later on.
	 */
	protected JButton addButton(String text, int xPos, int yPos, int width, int height, ActionListener listener) {
		JButton button = new JButton(text);
		button.setLocation(xPos, yPos);
		button.setSize(width, height);
		button.addActionListener(listener);
		this.add(button);
		return button;
	}
	
	/**
	 * Class that implements an actionlistener for the start rename button of the GUI
	 * @author Hermann Krumrey
	 *
	 */
	protected class StartButton implements ActionListener {
		/**
		 * The action performed by the button
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
			String[] newEpisodeNames = new String[episodes.length];
			promptForNewNames(episodes, newEpisodeNames);
			
			renamer.setNewEpisodeNames(newEpisodeNames);
			
			boolean confirmed = true;
			for (int i = 0; i < episodes.length; i++) {
				confirmed = confirmationPrompt(episodes[i], newEpisodeNames[i]);
				if (!confirmed) {break;}
			}
			
			if (!confirmed) {
				JOptionPane.showMessageDialog(MainGUI.this, "Operation aborted");
			} else {
				renamer.startRename();
			}	
		}
		
		/**
		 * Prompts the user for each new episode name in order
		 * @param episodes - array of episodes
		 * @param newEpisodeNames - array of new episode names
		 */
		private void promptForNewNames(Episode[] episodes, String[] newEpisodeNames) {
			for (int i = 0; i < episodes.length; i++) {
				JFrame frame = new JFrame("New Episode Name");
				String prompt = JOptionPane.showInputDialog(frame, "Enter the new episode name for: \n" + episodes[i].getName());
				newEpisodeNames[i] = prompt;
			}
		}
		
		/**
		 * Prompts the user for confirmation of an episode rename
		 */
		private boolean confirmationPrompt(Episode episode, String newName) {
			int confirmed = JOptionPane.YES_NO_OPTION;
			String message = "Rename\n\n" + episode.getName() + "\n\nto:\n\n";
			message += episode.getShowName() + " - S" + episode.getSeason() + "E" + episode.getEpisode();
			message += " - " + newName + "." + episode.getFileExtension() + "\n\n?";
			confirmed = JOptionPane.showConfirmDialog(MainGUI.this, message, "rename confirmation", confirmed);
			if (confirmed == 0) { return true; } else { return false; }
		}
	}
}
