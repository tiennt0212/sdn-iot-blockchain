from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."

        # Add hosts and switches
	h1 = self.addHost( 'h1' )
        h2 = self.addHost( 'h2' )

        s1 = self.addSwitch( 's1' )

        # Add links
        self.addLink( h1, s1 )
        self.addLink( h2, s1 )

topos = { 'mytopo': ( lambda: MyTopo() ) }
