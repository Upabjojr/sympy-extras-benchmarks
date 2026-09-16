%------------------------------------------------------------------------------
% File     : ARI616_1 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : If intervals intersect, then sum_of_radii >= distance_of_centers
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v7.3.0, 0.12 v7.1.0, 0.00 v6.2.0, 0.40 v6.1.0, 0.44 v6.0.0, 0.50 v5.3.0, 0.57 v5.2.0, 0.60 v5.1.0
% Syntax   : Number of formulae    :    2 (   0 unt;   1 typ;   0 def)
%            Number of atoms       :    6 (   0 equ)
%            Maximal formula atoms :    6 (   6 avg)
%            Number of connectives :    5 (   0   ~;   0   |;   2   &)
%                                         (   1 <=>;   2  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    9 (   9 avg)
%            Maximal term depth    :    3 (   1 avg)
%            Number arithmetic     :   17 (   3 atm;   6 fun;   0 num;   8 var)
%            Number of types       :    2 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    3 (   1   >;   2   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   1 usr;   0 prp; 2-3 aty)
%            Number of functors    :    2 (   0 usr;   0 con; 1-2 aty)
%            Number of variables   :    8 (   7   !;   1   ?;   8   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(p_type,type,
    p: ( $int * $int * $int ) > $o ).

tff(sum_of_radii_gt_distance_of_centers,conjecture,
    ( ! [X: $int,Y: $int,Z: $int] :
        ( ( $lesseq($sum(Y,$uminus(Z)),X)
          & $lesseq(X,$sum(Y,Z)) )
      <=> p(X,Y,Z) )
   => ! [Y1: $int,Z1: $int,Y2: $int,Z2: $int] :
        ( ? [X: $int] :
            ( p(X,Y1,Z1)
            & p(X,Y2,Z2) )
       => $lesseq($sum(Y1,$uminus(Y2)),$sum(Z1,Z2)) ) ) ).

%------------------------------------------------------------------------------
