package com.krumreyh.java.folder.icon.changer.objects;

import java.io.File;

import com.krumreyh.java.krumreylib.fileops.FileHandler;

/**
 * Class that models an icon
 * @author Hermann Krumrey
 * @version 1.0
 */
public class Icon {

	private File ico;
	private File png;
	private String name;
	
	/**
	 * Constructor that automatically generates PNG Files from ICO Files if none exist yet.
	 * @param iconFile - the original iconFile
	 */
	public Icon(File iconFile) {
		this.name = FileHandler.getPureFileName(iconFile);
		if (FileHandler.getExtension(iconFile).equals("ico")) {
			this.ico = iconFile;
			String pngPath = iconFile.getAbsolutePath().split(".ico")[0] + ".png";
			if (!FileHandler.checkIfFile(pngPath)) {
				//TODO Convert ICO to PNG
			}
			this.png = new File(pngPath);
		} else if (FileHandler.getExtension(iconFile).equals("png")) {
			this.png = iconFile;
			String icoPath = iconFile.getAbsolutePath().split(".png")[0] + ".ico";
			if (!FileHandler.checkIfFile(icoPath)) {
				//TODO Convert PNG to ICO
			}
			this.png = new File(icoPath);
		} else {
			//TODO Exception
		}
	}
}
