import math
import click
import halfedge_mesh

def dist(a, b):
    return math.sqrt(sum(map(lambda(x): (x[0] - x[1])**2, zip(a, b))))

def load_off_data(fn):
    with open(fn, 'r') as fp:
        lines = fp.readlines()
    lines = filter(lambda x: x.strip() != '' and x[0] != '#', lines)
    header, rest = lines[:2], lines[2:]
    vert_count = int(header[1].split()[0])
    verts, rest = rest[:vert_count], rest[vert_count:]
    return header, verts, rest

class MeshDiff:
    def __init__(self, mesh_a, mesh_b):
        """
        Compute the subset of a that is not in b
        """
        self.mesh_a = mesh_a
        self.mesh_b = mesh_b
        self.compute_inclusion_list()


    def compute_inclusion_list(self):
        """
        @Internal
        Compute the vertices that occur in a and b.

        Uses naive quadratic search over pairs of points.  You can speed this
        up by using a spatial data structure.
        """
        self.verts_in_a = {}
        self.verts_in_both = []
        for v in self.mesh_a.vertices:
            self.verts_in_a[tuple(v.get_vertex())] = v.index
        for v in map(lambda x : tuple(x.get_vertex()), self.mesh_b.vertices):
            if v in self.verts_in_a:
                self.verts_in_both.append(self.verts_in_a[v])
            else:
                found = None
                for p2 in self.verts_in_a:
                    if dist(v, p2) < 1e-3:
                        found = p2
                        break
                if found:
                    self.verts_in_both.append(self.verts_in_a[p2])

@click.group()
def cli():
    pass

@click.command()
@click.argument('mesh_a')
@click.argument('mesh_b')
@click.argument('output_ref')
def diff(mesh_a, mesh_b, output_ref):
    a = halfedge_mesh.HalfedgeMesh(mesh_a)
    b = halfedge_mesh.HalfedgeMesh(mesh_b)
    md = MeshDiff(a, b)
    with open(output_ref, 'w') as fp:
        fp.write("OFFDIFF\n")
        fp.write("%d\n" % len(md.verts_in_both))
        for k in md.verts_in_both:
            fp.write("%d\n" % k)
        header, verts, topology = load_off_data(mesh_b)
        fp.writelines(topology)

@click.command()
@click.argument('ref')
@click.argument('tgt_mesh')
@click.argument('output')
def push(ref, tgt_mesh, output):
    unused, inclusion_list, topology = load_off_data(ref)
    unused, verts, unused2 = load_off_data(tgt_mesh)
    inclusion_list = map(lambda x: int(x), inclusion_list)
    included_verts = []
    for vid in inclusion_list:
        included_verts.append(verts[vid])
    with open(output, 'w') as fp:
        fp.write("OFF\n")
        fp.write("%d %d 0\n" % (len(included_verts), len(topology)))
        fp.writelines(included_verts)
        fp.writelines(topology)

@click.command()
@click.argument('mesh_a')
@click.argument('mesh_b')
def check(mesh_a, mesh_b):
    a = halfedge_mesh.HalfedgeMesh(mesh_a)
    b = halfedge_mesh.HalfedgeMesh(mesh_b)
    va = set(map(lambda x: tuple(x.get_vertex()), a.vertices))
    for v in b.vertices:
        if not tuple(v.get_vertex()) in va:
            raise "Error"

cli.add_command(diff)
cli.add_command(check)
cli.add_command(push)

if __name__ == '__main__':
    cli()
