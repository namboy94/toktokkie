package com.krumreyh.java.folder.icon.changer.iconizers;

import java.io.File;
import java.io.IOException;

import com.krumreyh.java.krumreylib.fileops.FileHandler;

public class NautilusIconizer extends Iconizer{

	public NautilusIconizer(String directory) {
		this.construct(directory);
	}
	
	public void iconize() {
		this.iconize(new NautilusIconCommand());
	}
	
	private class NautilusIconCommand implements IconCommand {

		public void iconize(File folder, File iconFolder) {
			String folderName = folder.getName();
			String folderToChange = folder.getAbsolutePath();
			String folderIcon = iconFolder.getAbsolutePath() + FileHandler.getDivider(iconFolder) + folderName + ".png";
			String command = "gvfs-set-attribute -t string '" + folderToChange + "' metadata::custom-icon 'file://" + folderIcon + "'";
			try {
				Runtime.getRuntime().exec(new String[] {"/bin/sh", "-c", command});
			} catch (IOException e) {
				e.printStackTrace();
			}
		}

		public void iconize(File folder, File iconFolder, String special) {
			String folderToChange = folder.getAbsolutePath();
			String folderIcon = iconFolder.getAbsolutePath() + FileHandler.getDivider(iconFolder) + special + ".png";
			String command = "gvfs-set-attribute -t string '" + folderToChange + "' metadata::custom-icon 'file://" + folderIcon + "'";
			try {
				Runtime.getRuntime().exec(new String[] {"/bin/sh", "-c", command});
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}
}
