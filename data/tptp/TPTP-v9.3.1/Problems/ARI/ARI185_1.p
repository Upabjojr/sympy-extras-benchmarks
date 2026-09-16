%--------------------------------------------------------------------------
% File     : ARI185_1 : TPTP v9.3.1. Released v5.0.0.
% Domain   : Arithmetic
% Problem  : Integer: Positive function formula
% Version  : Especial.
% English  : 

% Refs     : [PW06]  Prevosto & Waldmann (2006), SPASS+T
%          : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    : (20) [PW06]

% Status   : Theorem
% Rating   : 0.00 v8.2.0, 0.17 v7.5.0, 0.00 v6.2.0, 0.20 v6.1.0, 0.33 v6.0.0, 0.38 v5.5.0, 0.50 v5.4.0, 0.62 v5.3.0, 0.71 v5.2.0, 1.00 v5.0.0
% Syntax   : Number of formulae    :    2 (   0 unt;   1 typ;   0 def)
%            Number of atoms       :    2 (   0 equ)
%            Maximal formula atoms :    2 (   2 avg)
%            Number of connectives :    1 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    3 (   3 avg)
%            Maximal term depth    :    4 (   2 avg)
%            Number arithmetic     :   10 (   2 atm;   2 fun;   5 num;   1 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    1 (   1   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    8 (   1 usr;   5 con; 0-2 aty)
%            Number of variables   :    1 (   1   !;   0   ?;   1   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments : 
%--------------------------------------------------------------------------
tff(f_type,type,
    f: $int > $int ).

tff(co1,conjecture,
    ( ! [U: $int] : $greater(f(U),1)
   => $less($difference(7,$product(2,f(3))),4) ) ).

%--------------------------------------------------------------------------
