%------------------------------------------------------------------------------
% File     : ARI596_1 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : There is a number in {a,a+1,a-1} that is divisible by 3
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : Theorem
% Rating   : 0.50 v9.1.0, 0.60 v9.0.0, 0.50 v8.2.0, 0.67 v7.5.0, 0.60 v7.4.0, 0.67 v7.3.0, 0.75 v7.1.0, 0.67 v7.0.0, 0.50 v6.4.0, 0.33 v6.3.0, 0.50 v6.2.0, 0.80 v6.1.0, 0.89 v6.0.0, 0.88 v5.4.0, 1.00 v5.1.0
% Syntax   : Number of formulae    :    3 (   0 unt;   2 typ;   0 def)
%            Number of atoms       :    4 (   0 equ)
%            Maximal formula atoms :    4 (   4 avg)
%            Number of connectives :    3 (   0   ~;   0   |;   2   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    4 (   4 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number arithmetic     :    7 (   0 atm;   3 fun;   3 num;   1 var)
%            Number of types       :    2 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    1 (   1   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   1 usr;   0 prp; 1-1 aty)
%            Number of functors    :    6 (   1 usr;   3 con; 0-2 aty)
%            Number of variables   :    1 (   0   !;   1   ?;   1   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments : Also a theorem for $rat and $real, but much easier
%------------------------------------------------------------------------------
tff(p_type,type,
    p: $int > $o ).

tff(a_type,type,
    a: $int ).

tff(exists_X_in_a_aplus1_aminus1_div_3,conjecture,
    ( ( p(a)
      & p($sum(a,1))
      & p($difference(a,1)) )
   => ? [X: $int] : p($product(3,X)) ) ).

%------------------------------------------------------------------------------
