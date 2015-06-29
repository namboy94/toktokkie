package com.krumreyh.java.folder.icon.changer.iconizers;

import java.io.File;
import java.io.InputStream;

import com.krumreyh.java.krumreylib.fileops.FileHandler;

/**
 * Class that handles the iconizing of folders
 * @author Hermann Krumrey
 * @version 1.0
 */
public abstract class Iconizer {

	protected File[] children;
	
	/**
	 * Constructor-method that checks if the give directory is valid and saves its children to a File array
	 * @param directory - the directory containing all shows to be iconized
	 * @throws IllegalArgumentException - in case the directory is invalid
	 */
	protected void construct(String directory) throws IllegalArgumentException {
		if (!FileHandler.checkIfDirectory(directory)) {
			throw new IllegalArgumentException("Not a valid directory");
		}
		this.children = FileHandler.getChildrenDirectories(directory);
	}
	
	/**
	 * Starts the iconizing of all child directories
	 * @param iconcom - the IconCommand object, operates differently depending on OS and file browser
	 */
	protected void iconize(IconCommand iconcom) {
		for (int i = 0; i < this.children.length; i++) {
			File folderIconFolder = null;
			File[] innerChildren = FileHandler.getChildrenDirectories(this.children[i]);
			for (int j = 0; j < innerChildren.length; j++) {
				if (innerChildren[j].getName().equals("Folder Icon")) {
					folderIconFolder = innerChildren[j];
					convertMissingIcons(folderIconFolder, iconcom);
					copyDefaultIcons(folderIconFolder, innerChildren);
					break;
				}
			}
			iconcom.iconize(this.children[i], folderIconFolder, "Main");
			iconcom.iconize(folderIconFolder, folderIconFolder, "Folder");
			for (int j = 0; j < innerChildren.length; j++) {
				if (innerChildren[j].getName().equals("Folder Icon")) {
					continue;
				}
				if (FileHandler.checkIfDirectory(innerChildren[j])) {
					iconcom.iconize(innerChildren[j], folderIconFolder);
					if (FileHandler.hasChildren(innerChildren[j])) {
						recursiveIconize(innerChildren[j], iconcom, folderIconFolder);
					}
				}
			}
		}
	}
	
	/**
	 * Recursively changes the folder icon of all directories in a directory
	 * @param directory - the directory whose subdirectories' folder icons should be changed
	 * @param iconcom - the icon command
	 * @param folderIconFolder - the directory where the folder icons are located
	 */
	protected void recursiveIconize(File directory, IconCommand iconcom, File folderIconFolder) {
		File[] children = FileHandler.getChildrenDirectories(directory);
		for (int i = 0; i < children.length; i++) {
			if (FileHandler.checkIfDirectory(children[i])) {
				iconcom.iconize(children[i], folderIconFolder);
				if (FileHandler.hasChildren(children[i])) {
					recursiveIconize(children[i], iconcom, folderIconFolder);
				}
			}
		}
	}
	
	/**
	 * Copies default icon files to the folder icon directory in case they are not there yet.
	 * @param folderIconFolder - the folder icon folder where the default icons should be copied to.
	 * TODO @param siblingDirectories - Array of directories on the same plane as a the folder icon folder
	 */
	protected void copyDefaultIcons(File folderIconFolder, File[] siblingDirectories) {
		String[] resources = new String[] {	"Subbed SD", "Subbed 720p", "Subbed 1080p",
											"Dual-Audio SD", "Dual-Audio 720p", "Dual-Audio 1080p",
											"Multi-Audio SD", "Multi-Audio 720p", "Multi-Audio 1080p",
											"Dubbed SD", "Dubbed 720p", "Dubbed 1080p",
											"Folder", "Main"};
		
		String folderIconDirectory = folderIconFolder.getAbsolutePath() + FileHandler.getDivider(folderIconFolder);
		
		for (int i = 0; i < resources.length; i++) {
			String ico = resources[i] + ".ico";
			String png = resources[i] + ".png";
			boolean icoFound = false;
			boolean pngFound = false;
			File[] icons = FileHandler.getDirectoryContent(folderIconFolder);
			for (int j = 0; j < icons.length; j++) {
				if (icons[j].getName().equals(ico)) {
					icoFound = true;
				} else if (icons[j].getName().equals(png)) {
					pngFound = true;
				}
			}
			if (!icoFound) {
				FileHandler.copyResource("/" + ico, new File(folderIconDirectory + ico));
			}
			if (!pngFound) {
				FileHandler.copyResource("/" + png, new File(folderIconDirectory + png));
			}
		}
		
		//TODO Optimize Code, maybe merge the two processes, or at least thread it.
		
		File[] folderIcons = FileHandler.getDirectoryContent(folderIconFolder);
		
		for (int i = 0; i < siblingDirectories.length; i++) {
			if (FileHandler.getPureFileName(siblingDirectories[i]).equals("Folder Icon")) {
				continue;
			}
			boolean foundIco = false;
			boolean foundPng = false;
			for (int j = 0; j < folderIcons.length; j++) {
				if (FileHandler.getPureFileName(folderIcons[j]).equals(FileHandler.getPureFileName(siblingDirectories[i]))){
					if (FileHandler.getExtension(folderIcons[i]).equals("ico")) {
						foundIco = true;
					} else if (FileHandler.getExtension(folderIcons[i]).equals("png")) {
						foundPng = true;
					}
					if (foundPng && foundIco) {
						break;
					}
				}
			}
			String nameOfSibling = FileHandler.getPureFileName(siblingDirectories[i]);
			if (!foundIco) {
				FileHandler.copyResource("/Main.ico", new File(folderIconDirectory + nameOfSibling + ".ico"));
			}
			if (!foundPng) {
				FileHandler.copyResource("/Main.png", new File(folderIconDirectory + nameOfSibling + ".png"));
			}
		}
	}
	
	protected void convertMissingIcons(File folderIconFolder, IconCommand iconcom) {
		File[] icons = FileHandler.getDirectoryContent(folderIconFolder);
		for (int i = 0; i < icons.length; i++) {
			boolean foundPair = false;
			String name = FileHandler.getPureFileName(icons[i]);
			for (int j = 0; j < icons.length; j++) {
				if (i == j) {
					continue;
				}
				if (FileHandler.getPureFileName(icons[j]).equals(name)) {
					foundPair = true;
					break;
				}
			}
			if (!foundPair) {
				iconcom.convert(icons[i], folderIconFolder);
			}
		}
	}
	
	/**
	 * Interface that handles the actual iconizing of folders
	 */
	protected interface IconCommand {
		
		/**
		 * Iconizes a folder
		 * @param folder - the folder to be iconized
		 * @param iconFolder = the directory containing the folder icons
		 */
		void iconize(File folder, File iconFolder);
		
		/**
		 * Iconizes a special folder
		 * @param folder - the folder to be iconized
		 * @param iconFolder = the directory containing the folder icons
		 * @param special - indicates the type of folder
		 */
		void iconize(File folder, File iconFolder, String special);
		
		/**
		 * Converts an icon (png -> ico, ico -> png)
		 * @param original - the original icon file
		 * @param parent - the parent directory of the file
		 */
		void convert(File original, File parent);
	}
	
}
