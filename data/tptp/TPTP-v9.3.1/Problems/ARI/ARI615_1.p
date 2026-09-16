%------------------------------------------------------------------------------
% File     : ARI615_1 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : If Z<=W, then [X-Z,X+Z] is a subset of [X-W,X+W]
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v7.3.0, 0.12 v7.1.0, 0.00 v6.2.0, 0.40 v6.1.0, 0.44 v6.0.0, 0.50 v5.4.0, 0.62 v5.3.0, 0.71 v5.2.0, 0.80 v5.1.0
% Syntax   : Number of formulae    :    2 (   0 unt;   1 typ;   0 def)
%            Number of atoms       :    6 (   0 equ)
%            Maximal formula atoms :    6 (   6 avg)
%            Number of connectives :    5 (   0   ~;   0   |;   1   &)
%                                         (   1 <=>;   3  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    8 (   8 avg)
%            Maximal term depth    :    3 (   1 avg)
%            Number arithmetic     :   13 (   3 atm;   3 fun;   0 num;   7 var)
%            Number of types       :    2 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    3 (   1   >;   2   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   1 usr;   0 prp; 2-3 aty)
%            Number of functors    :    2 (   0 usr;   0 con; 1-2 aty)
%            Number of variables   :    7 (   7   !;   0   ?;   7   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(p_type,type,
    p: ( $int * $int * $int ) > $o ).

tff(interv_with_smaller_radius_contained,conjecture,
    ( ! [X: $int,Y: $int,Z: $int] :
        ( ( $lesseq($sum(Y,$uminus(Z)),X)
          & $lesseq(X,$sum(Y,Z)) )
      <=> p(X,Y,Z) )
   => ! [X: $int,Y: $int,Z: $int,W: $int] :
        ( $lesseq(Z,W)
       => ( p(X,Y,Z)
         => p(X,Y,W) ) ) ) ).

%------------------------------------------------------------------------------
