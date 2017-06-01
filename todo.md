# TODO LIST

## New Features
- Assign layup for closed shapes.
- When assigning a layup, pick area by set name.
- Ply manager.
- Generate XML parameter files from GUI for future reuse.
- Run VABS analysis from CAE directly, without creating the job and input file.
- Create a shortcut with sc/vabs logo.
- ~~Mesh control in parametric input file.~~

## Bug Fix
- **PREPARE EXAMPLES FOR DEBUGGING.**
- Show warning or error messages.
- Cannot import materials or layups alone.
- 'Feature creation failed' when assign layup with only one layer.

## Optimization
- **MERGE THE TWO GUIs.**
  - Homogenization
  - Dehomogenization
- ~~Redesign the VABS logo.~~
- ~~Better parsing process for Abaqus input.~~
- Better way to store layer information (material id/name + fiber orientation)
- Change the format of layup input file to xml for the 'Read from file' method in the 1D structure genome.
- Unify the titles, texts, names and notes used in the GUI (button, dialog box, label, etc.).
