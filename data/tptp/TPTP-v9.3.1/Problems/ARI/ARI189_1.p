%--------------------------------------------------------------------------
% File     : ARI189_1 : TPTP v9.3.1. Released v5.0.0.
% Domain   : Arithmetic
% Problem  : Integer: Product of 2 and something is 10 in a predicate
% Version  : Especial.
% English  : 

% Refs     : [PW06]  Prevosto & Waldmann (2006), SPASS+T
%          : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    : (25) [PW06]

% Status   : Theorem
% Rating   : 0.00 v9.1.0, 0.20 v9.0.0, 0.00 v8.2.0, 0.17 v7.5.0, 0.00 v7.3.0, 0.25 v7.1.0, 0.00 v7.0.0, 0.17 v6.4.0, 0.33 v6.3.0, 0.25 v6.2.0, 0.60 v6.1.0, 0.67 v6.0.0, 0.75 v5.5.0, 0.88 v5.4.0, 0.62 v5.3.0, 0.71 v5.2.0, 0.80 v5.1.0, 0.75 v5.0.0
% Syntax   : Number of formulae    :    2 (   0 unt;   1 typ;   0 def)
%            Number of atoms       :    2 (   0 equ)
%            Maximal formula atoms :    2 (   2 avg)
%            Number of connectives :    1 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    3 (   3 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number arithmetic     :    4 (   0 atm;   1 fun;   2 num;   1 var)
%            Number of types       :    2 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    1 (   1   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   1 usr;   0 prp; 1-1 aty)
%            Number of functors    :    3 (   0 usr;   2 con; 0-2 aty)
%            Number of variables   :    1 (   1   !;   0   ?;   1   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments : 
%--------------------------------------------------------------------------
tff(p_type,type,
    p: $int > $o ).

tff(co1,conjecture,
    ( ! [U: $int] : p($product(2,U))
   => p(10) ) ).

%--------------------------------------------------------------------------
