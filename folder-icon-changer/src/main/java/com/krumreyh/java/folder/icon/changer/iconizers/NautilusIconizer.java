package com.krumreyh.java.folder.icon.changer.iconizers;

import java.io.File;
import java.io.IOException;

import com.krumreyh.java.krumreylib.cli.TerminalParser;
import com.krumreyh.java.krumreylib.fileops.FileHandler;

/**
 * Class that handles Iconizing for the Nautilus File Browser (available on GNU/Linux-Systems)
 * This Iconizer class also works for Nemo, Linux Mint's default file browser
 * This is the default Iconizer for Linux
 * @author Hermann Krumrey
 * @version 1.0
 */
public class NautilusIconizer extends Iconizer {

	/**
	 * Constructor that makes use of the Iconizer class's construct class
	 * @param directory - the directory to be used
	 */
	public NautilusIconizer(String directory) {
		this.construct(directory);
	}
	
	/**
	 * Starts the iconizing process specifically for the Nautilus File Browser
	 */
	public void iconize() {
		this.iconize(new NautilusIconCommand());
	}
	
	/**
	 * The IconCommand that handles the actual system calls to change the folder icon
	 */
	private class NautilusIconCommand implements IconCommand {

		public void iconize(File folder, File iconFolder) {
			String folderName = folder.getName();
			if (folderName.endsWith("+")) {
				folderName = folderName.substring(0, folderName.length() - 1);
			}
			String folderToChange = folder.getAbsolutePath();
			String folderIcon = iconFolder.getAbsolutePath() + FileHandler.getDivider(iconFolder) + folderName + ".png";
			changeIcon(folderToChange, folderIcon);
		}

		public void iconize(File folder, File iconFolder, String special) {
			String folderToChange = folder.getAbsolutePath();
			String folderIcon = iconFolder.getAbsolutePath() + FileHandler.getDivider(iconFolder) + special + ".png";
			changeIcon(folderToChange, folderIcon);
		}
		
		/**
		 * Changes the icon of a single folder
		 * @param folder - the folder whose icon should be changed
		 * @param icon - the icon to be used
		 */
		private void changeIcon(String folder, String icon) {
			String command = "gvfs-set-attribute -t string '" + folder
					+ "' metadata::custom-icon 'file://" + icon + "'";
			try {
				Runtime.getRuntime().exec(new String[] {"/bin/sh", "-c", command});
			} catch (IOException e) {
			}
		}

		public void convert(File original, File parent) {
			String path = parent.getAbsolutePath() + FileHandler.getDivider(parent);
			String name = FileHandler.getPureFileName(original);
			String ext = FileHandler.getExtension(original);
			String ico = path + name + ".ico";
			String png = path + name + ".png";
			try {
				if (ext.equals("png")) {
					String command = "convert \"" + png + "\" \"" + ico + "\"";
					Runtime.getRuntime().exec(new String[] {"/bin/sh", "-c", command});
				} else if (ext.equals("ico")) {
					String command = "convert \"" + ico + "\" \"" + png + "\"";
					Runtime.getRuntime().exec(new String[] {"/bin/sh", "-c", command}).waitFor();
					icoConvertCleanup(name, path, parent);
				}
			} catch (IOException | InterruptedException e) {
			}
		}
		
		private void icoConvertCleanup(String name, String path, File parent) {
			File[] icons = FileHandler.getDirectoryContent(parent);
			File[] newIcons = new File[icons.length];
			int i = 0;
			for (int j = 0; j < icons.length; j++) {
				if (icons[j].getName().contains(name) && FileHandler.getExtension(icons[j]).equals("png")) {
					newIcons[i] = icons[j];
					i++;
				}
			}
			File largest = newIcons[0];
			for (int j = 0; j < newIcons.length; j++) {
				if (newIcons[j] == null) {
					break;
				}
				if (newIcons[j].length() > largest.length()) {
					largest.delete();
					largest = newIcons[j];
				} else {
					if (j > 0) {
						newIcons[j].delete();
					}
				}
			}
			FileHandler.renameFile(largest, name);
		}
	}
}
