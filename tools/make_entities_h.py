# Creates C data structures for binary lookup table of entities,
# using python's html5 entity data.
# Usage: python3 tools/make_entities_h.py > src/entities.h

import html

entities5 = html.entities.html5

# remove keys without semicolons.  For some reason the list
# has duplicates of a few things, like auml, one with and one
# without a semicolon.
entities = sorted([(k[:-1], entities5[k].encode('utf-8')) for k in entities5.keys() if k[-1] == ';'])

# Print out the header:
print("""#ifndef CMARK_ENTITIES_H
#define CMARK_ENTITIES_H

#ifdef __cplusplus
extern "C" {
#endif

struct cmark_entity_node {
	unsigned char *entity;
        unsigned char bytes[8];
};

#define CMARK_ENTITY_MIN_LENGTH 2
#define CMARK_ENTITY_MAX_LENGTH 31""")

print("#define CMARK_NUM_ENTITIES " + str(len(entities)));

print("\nstatic const struct cmark_entity_node cmark_entities[] = {");

for (ent, bs) in entities:
  print('{(unsigned char*)"' + ent + '", {' + ', '.join(map(str, bs)) + ', 0}},')

print("};\n");

print("""
#ifdef __cplusplus
}
#endif

#endif
""")
