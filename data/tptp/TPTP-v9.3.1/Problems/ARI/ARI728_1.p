%------------------------------------------------------------------------------
% File     : ARI728_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : If 2*X is an integer, then X is an integer or X+0.5 is an integer
% Version  : Especial.
% English  :

% Refs     : [Wal14] Waldmann (2014), Email to Geoff Sutcliffe
% Source   : [Wal14]
% Names    : 

% Status   : Theorem
% Rating   : 1.00 v7.5.0, 0.80 v7.4.0, 0.83 v7.3.0, 0.88 v7.1.0, 0.83 v6.4.0, 0.33 v6.3.0
% Syntax   : Number of formulae    :    1 (   0 unt;   0 typ;   0 def)
%            Number of atoms       :    3 (   0 equ)
%            Maximal formula atoms :    3 (   3 avg)
%            Number of connectives :    2 (   0   ~;   1   |;   0   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    4 (   4 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number arithmetic     :    8 (   3 atm;   2 fun;   2 num;   1 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 1-1 aty)
%            Number of functors    :    4 (   0 usr;   2 con; 0-2 aty)
%            Number of variables   :    1 (   1   !;   0   ?;   1   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments : 
%------------------------------------------------------------------------------
tff(prove,conjecture,
    ! [X: $real] :
      ( $is_int($product(2.0,X))
     => ( $is_int(X)
        | $is_int($sum(X,0.5)) ) ) ).

%------------------------------------------------------------------------------
