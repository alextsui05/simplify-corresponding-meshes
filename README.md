# Simplify Corresponding Meshes

Give a set of corresponding meshes this can simplifya mesh and push
that change to the rest of the meshes.

## Prerequisites
    meshlabserver is on the PATH
    $> pip install click

## Quick example

 1. ./simplify_mesh.sh straight.off 1000 straight1k.off
 2. python mesh_diff.py diff straight.off straight1k.off 1k.ref
 3. python mesh_diff.py push 1k.ref twisted.off twisted1k.off

where

  1. simplifies one mesh
  2. creates a diff between the simplified mesh and the full resolution mesh
  3. push the changes to the whole dataset 
