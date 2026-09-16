%------------------------------------------------------------------------------
% File     : ARI587_1 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : For X > 1, there is a Y between X+2 and 3X (e.g., Y = 2X + 1)
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v7.4.0, 0.17 v7.3.0, 0.25 v7.1.0, 0.17 v7.0.0, 0.00 v6.1.0, 0.22 v6.0.0, 0.25 v5.3.0, 0.43 v5.2.0, 0.60 v5.1.0
% Syntax   : Number of formulae    :    1 (   0 unt;   0 typ;   0 def)
%            Number of atoms       :    3 (   0 equ)
%            Maximal formula atoms :    3 (   3 avg)
%            Number of connectives :    2 (   0   ~;   0   |;   1   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    5 (   5 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number arithmetic     :   10 (   3 atm;   2 fun;   3 num;   2 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    5 (   0 usr;   3 con; 0-2 aty)
%            Number of variables   :    2 (   1   !;   1   ?;   2   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(exists_Y_between_Xplus2_and_3X,conjecture,
    ! [X: $int] :
      ( $less(1,X)
     => ? [Y: $int] :
          ( $less($sum(X,2),Y)
          & $less(Y,$product(X,3)) ) ) ).

%------------------------------------------------------------------------------
