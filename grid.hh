// grid.hh C++11
// Part of the robots project
// Author: Dirk Oliver Theis
#ifndef __ROBOT__GRID_HH__
#define __ROBOT__GRID_HH__

#include <stdexcept>
#include <vector>

namespace GridSpace {

    // Grid coordinates
    struct XY {
        short x;
        short y;
        inline constexpr XY(short _x=-1, short _y=-1): x{_x}, y{_y}  {}
    }; // struct XY

    constexpr XY nowhere {-1,-1};

    inline    bool operator == (XY xy, XY uv) { return xy.x==uv.x && xy.y==uv.y ; }
    inline    bool operator != (XY xy, XY uv) { return xy.x!=uv.x || xy.y!=uv.y ; }



    //  movement unaware of the grid:

    inline XY blind_east (XY xy) { return XY{ (short)(xy.x+1),          xy.y    };  }
    inline XY blind_north(XY xy) { return XY{         xy.x,     (short)(xy.y+1) };  }
    inline XY blind_west (XY xy) { return XY{ (short)(xy.x-1),          xy.y    };  }
    inline XY blind_south(XY xy) { return XY{         xy.x,     (short)(xy.y-1) };  }


    enum class Direction : char { east, north, west, south };

    inline XY blind_move(XY now, Direction d) {
        switch(d) {
        case Direction::east:  return blind_east(now);
        case Direction::north: return blind_north(now);
        case Direction::west:  return blind_west(now);
        case Direction::south: return blind_south(now);
        default: throw std::runtime_error("blind_move(): illegal direction");
        }
    } //^ blind_move()


    //******************************************************************************************************************************************************
    //  The grid

    union Node_type {
        struct {
            bool east  : 1;      // (+1,0)
            bool north : 1;      // (0,+1)
            bool west  : 1;      // (-1,0)
            bool south : 1;      // (0,-1)
        };
        char raw;
        Node_type( const std::vector<Direction> & dlist ): raw{0} { for (Direction d : dlist) { switch(d) { case Direction::north: north=true; break; case Direction::south: south=true; break; case Direction::east: east=true; break; case Direction::west: west=true; } } }
        Node_type(char _r=0): raw{_r} {}
    }; // union Node_type

    struct Grid {
        const short NS, EW;

        template<typename T>
        struct vector_grid: public std::vector<T> {
            const Grid & G;
            inline const T & operator[](XY xy) const { return std::vector<T>::operator[](G.idx(xy.x,xy.y)); }
            inline       T & operator[](XY xy)       { return std::vector<T>::operator[](G.idx(xy.x,xy.y)); }
            vector_grid(const Grid & _G): std::vector<T>(_G.sz()), G{_G} {}
        };

        inline bool      exists (XY xy)   const      { return exists(xy.x,xy.y); }
        inline Node_type query  (XY xy)   const      { return query(xy.x,xy.y); }

        inline short NS_sz()            const        { return NS; }
        inline short EW_sz()            const        { return EW; }
        inline bool  in_range (XY xy)   const        { return in_range(xy.x,xy.y); }

        inline XY east (XY xy) const  { return ( query(xy).east  ?    blind_east (xy) : nowhere ); }
        inline XY north(XY xy) const  { return ( query(xy).north ?    blind_north(xy) : nowhere ); }
        inline XY south(XY xy) const  { return ( query(xy).south ?    blind_south(xy) : nowhere ); }
        inline XY west (XY xy) const  { return ( query(xy).west  ?    blind_west (xy) : nowhere ); }

        inline XY move (XY xy, Direction d) const;


        inline unsigned numo_slots() const  { if (numo_slots_storage>=0) return numo_slots_storage; numo_slots_storage=0;       for(short y=0; y<NS; ++y) for(short x=0;x<EW;++x) numo_slots_storage+=exists(x,y); return numo_slots_storage; }


        std::string print(char h_sep=' ',  char h_wall='|',
                          char v_sep=' ',  char v_wall='-',
                          char x_sep='+',  char x_wall='+',
                          char exist=' ',  char notexist='#')       const;
        unsigned    print_idx(XY xy, bool hi)   const  { return (3*NS-(3*xy.y+1+hi))*(2*EW+2)+2*xy.x+1; }

        Grid(const Grid &)=delete;

        std::string raw_write() const;

        ~Grid() { delete[] data; }
    protected:
        inline unsigned  sz()                          const      { return NS*EW; }

        inline bool      in_range (short x, short y)   const      { return x>=0 && y>=0 && x<EW && y<NS; }
        inline int       idx      (short x, short y)   const;

        inline bool      exists   (short x, short y)   const      { return in_range(x,y) && query(x,y).raw; }  // if a slot exists, then there should be a direction from which to access it.
        inline Node_type query    (short x, short y)   const      { return data[idx(x,y)]; }

        Node_type *data;
        Grid(short _NS, short _EW): NS(_NS), EW(_EW), data {new Node_type[sz()]}, numo_slots_storage(-1) { if (NS<=0 || EW<=0) throw std::range_error("Grid(): NS and EW must be positive."); }
    private:
        mutable int numo_slots_storage;
    }; // class Grid


    //******************************************************************************************************************************************************
    void check_Grid_consistency(const Grid &, std::string whos_asking="");

    struct Full_Rectangle__Grid: public Grid {
        Full_Rectangle__Grid(short _NS, short _EW);
    };

    struct Random__Grid: public Grid {
        Random__Grid(short _NS, short _EW, double NS_edge_probability, double EW_edge_probability); // if (p_EW<=0) p_EW=p_NS;
        Random__Grid(short _NS, short _EW, double slot_probability);
    };

    struct Read_From_Raw_Data__Grid: public Grid {
        Read_From_Raw_Data__Grid(short _NS, short _EW, const std::string &raw);
    };
} // namespace Grid


inline
int GridSpace::Grid::idx(short x, short y) const
{
# ifdef ROBOT_DEBUG
    if (!in_range(x,y)) throw std::range_error("Grid::idx():  coordinate out of range.");
# endif
    return EW*y + x;
} // Grid::idx()

inline
GridSpace::XY GridSpace::Grid::move (GridSpace::XY xy, GridSpace::Direction d) const
{
    switch(d) {
    case Direction::east:  return east(xy);
    case Direction::north: return north(xy);
    case Direction::west:  return west(xy);
    case Direction::south: return south(xy);
    default: throw std::runtime_error("GridSpace::Grid::move(): illegal direction");
    }
} //^ move()

#endif
// ^grid.hh EOF
