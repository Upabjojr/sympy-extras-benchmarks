%------------------------------------------------------------------------------
% File     : ARI731_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : If X is an integer, then 2*X+3 is an integer
% Version  : Especial.
% English  :

% Refs     : [Wal14] Waldmann (2014), Email to Geoff Sutcliffe
% Source   : [Wal14]
% Names    : 

% Status   : Theorem
% Rating   : 0.75 v9.1.0, 0.80 v9.0.0, 0.75 v8.2.0, 0.83 v7.5.0, 0.60 v7.4.0, 0.67 v7.3.0, 0.75 v7.1.0, 0.67 v6.4.0, 0.33 v6.3.0
% Syntax   : Number of formulae    :    1 (   0 unt;   0 typ;   0 def)
%            Number of atoms       :    2 (   0 equ)
%            Maximal formula atoms :    2 (   2 avg)
%            Number of connectives :    1 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    3 (   3 avg)
%            Maximal term depth    :    3 (   2 avg)
%            Number arithmetic     :    7 (   2 atm;   2 fun;   2 num;   1 var)
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
      ( $is_int(X)
     => $is_int($sum($product(X,2.0),3.0)) ) ).

%------------------------------------------------------------------------------
