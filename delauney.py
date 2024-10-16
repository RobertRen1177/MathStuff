from scipy.spatial import Delaunay
import numpy as np

def get_triangulation_from_cones(cones):
  """Gets a Delauney triangulation object given an array of cone coordinates

  Parameters
  ----------
  cones: Array of cone coordinates (e.g [[x1,y1], [x2,y2], etc...])

  Returns
  -------
  Triangulation object given by scipy
  """
  return Delaunay(cones)

def get_midpoint(p1, p2):
  """Returns the midpoint of two given points
  
  Parameters
  ----------
  p1: the first point [x1, y1]

  p2: the second point [x2, y2]

  Returns
  -------
  The midpoint as a tuple (x,y)
  """
  return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

def get_triangle_containing_point(point, cones, triangulation):
  """Given a point, return the triangle from the constructed Delauney triangulation
  that contains that point

  Parameters
  ----------
  point: the point that the triangle should contain

  cones: a list of all the cones that make up the Delauney triangulation

  triangulation: the Delauney triangulation object generated from the cones

  Returns
  -------  
  A tuple containing three points of a triangle (x1, y1), (x2, y2), (x3, y3)  
  """
  indices = triangulation.simplices[triangulation.find_simplex(point)]
  return cones[indices[0]], cones[indices[1]], cones[indices[2]]

def get_triangles_from_triangulation(triangulation, cones):
  """Given a triangulation object and a cones array, returns all the triangles
  formed by the triangulation
  
  Parameters
  ----------
  triangulation: the Delauney triangulation object that generated the triangles

  cones: a list of all the cones that make up the Delauney triangulation

  Returns
  -------
  A set where each element is three points (the points that make up the triangles)
  """
  tri = triangulation.simplices
  triangles = []
  for t in tri:
    triangles.append([cones[t[0]], cones[t[1]], cones[t[2]]])
  return triangles

def generate_edges_from_triangles(triangles):
  """Given a list where each element contains the coordinates of a triangle
  returned by Delauney triangulation, returns a list of edges where each
  element contains the two endpoints of the edge
  
  Parameters
  ----------
  triangles: a list of the triangles from Delauney triangulation.
  each element contains the three vertices of a triangle

  Returns
  -------
  A list of all the triangle edges, where each element contains the
  start and end point of the edge
  """
  edges = []
  for triangle in triangles:
    edges.append((triangle[0], triangle[1]))
    edges.append((triangle[0], triangle[2]))
    edges.append((triangle[1], triangle[2]))
  return edges

def find_internal_edges(edges, cones):
  """Given a list of all Delauney triangle edges and the list of cone coordinates,
  returns the triangle edges that are contained within the implicit track
  bounds formed by the cones (the internal edges).

  Parameters
  ----------
  edges: a list of all the triangle edges, from which the internal edges will be found.

  cones: array of cone coordinates (e.g [[x1,y1], [x2,y2], etc...]).
           The yellow and blue cones alternate positions in the array.

  Returns
  -------
  A list of all the internal triangle edges, where each element contains the
  start and end point of the edge
  """
  internal_edges = []

  yellow_cones = {tuple(cone) for cone in cones[::2]}
  blue_cones = {tuple(cone) for cone in cones[1::2]}
  for edge in edges:
    if (tuple(edge[0]) in yellow_cones and tuple(edge[1]) in blue_cones) or (tuple(edge[0]) in blue_cones and tuple(edge[1]) in yellow_cones):
      internal_edges.append(edge)
  return internal_edges

def find_midpoints_of_internal_edges(edges):
  """Given a list of all Delauney triangle internal edges, returns a list of the midpoints
  of all the internal triangle edges.

  Parameters
  ----------
  edges: a list of all the internal triangle edges, from which the midpoints will be found.

  Returns
  -------
  A list of all midpoints of the internal triangle edges, where each element is an (x,y) coordinate point
  """
  midpoints = []
  for edge in edges:
    midpoints.append(get_midpoint(edge[0], edge[1]))
  return midpoints

def combine_yellow_and_blue_cones(yellow_cones, blue_cones):
  """Combines a list of yellow cones and a list of blue cones into one list where
  yellow and blue cones alternate
  
  Parameters
  ----------
  yellow_cones: the list of yellow cone coordinates (e.g [[x1,y1], [x2,y2], etc...])

  blue_cones: the list of blue cone coordinates (e.g [[x1,y1], [x2,y2], etc...])

  Returns
  -------
  Array of alternating yellow and blue cones
  """
  return np.array([m for z in zip(yellow_cones, blue_cones) for m in z])